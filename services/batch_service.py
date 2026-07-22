import datetime
import math
import re
from models.batch import BatchModel
from models.course import CourseModel
from models.trainer import get_trainer_by_id, get_all_calendar_events


class BatchService:

    def __init__(self):
        self.batch_model = BatchModel()
        self.course_model = CourseModel()

    def generate_batch_code(self):
        """
        Generates a unique default batch code in format BATCH-YYYY-XXX.
        """
        year = datetime.datetime.now().year
        batches = self.batch_model.get_all_batches()
        count = len(batches) + 1
        code = f"BATCH-{year}-{count:03d}"
        
        # Ensure uniqueness
        while self.batch_model.batch_code_exists(code):
            count += 1
            code = f"BATCH-{year}-{count:03d}"
            
        return code

    def _check_trainer_skill_alignment(self, trainer_skills, course_tech_stack):
        """
        Checks if trainer skills overlap with course technology stack.
        """
        if not trainer_skills or not course_tech_stack:
            return True

        stop_words = {'and', 'or', '&', 'for', 'in', 'with', 'the', 'a', 'an'}
        t_tokens = {tok for tok in re.split(r'[,;/|\s]+', trainer_skills.lower()) if tok and tok not in stop_words}
        c_tokens = {tok for tok in re.split(r'[,;/|\s]+', course_tech_stack.lower()) if tok and tok not in stop_words}

        return bool(t_tokens.intersection(c_tokens))

    def calculate_end_date(self, course_id, start_date_str, slot_type):
        """
        Calculates estimated end date and project submission date based on Course duration,
        Slot Type, skipping weekends and calendar_event public holidays.
        """
        if not course_id or not start_date_str or not slot_type:
            return None

        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid start date format. Expected YYYY-MM-DD.")

        course = self.course_model.get_course_by_id(course_id)
        if not course:
            raise ValueError("Course not found.")

        duration_hours = course.get("duration_hours", 40)

        # Retrieve public holidays
        holidays = set()
        try:
            events = get_all_calendar_events()
            for ev in events:
                if dict(ev).get("event_type") == "Public Holiday":
                    holidays.add(dict(ev).get("date"))
        except Exception:
            holidays = set()

        # Determine hours per session and active days
        if "Weekend" in slot_type:
            daily_hours = 6.0
            is_weekend_slot = True
        else:
            daily_hours = 2.0
            is_weekend_slot = False

        total_sessions = math.ceil(duration_hours / daily_hours)
        current_date = start_date
        sessions_counted = 0

        max_days = 365 * 2
        days_iterated = 0

        while sessions_counted < total_sessions and days_iterated < max_days:
            weekday = current_date.weekday()  # 0: Mon ... 5: Sat, 6: Sun
            date_str = current_date.strftime("%Y-%m-%d")
            is_holiday = date_str in holidays

            if is_weekend_slot:
                if weekday in (5, 6) and not is_holiday:
                    sessions_counted += 1
            else:
                if weekday < 5 and not is_holiday:
                    sessions_counted += 1

            if sessions_counted < total_sessions:
                current_date += datetime.timedelta(days=1)

            days_iterated += 1

        end_date_str = current_date.strftime("%Y-%m-%d")

        # Project submission buffer: 5 working days after end_date
        proj_date = current_date + datetime.timedelta(days=1)
        working_days = 0
        p_days_iterated = 0

        while working_days < 5 and p_days_iterated < max_days:
            p_weekday = proj_date.weekday()
            p_date_str = proj_date.strftime("%Y-%m-%d")
            p_is_holiday = p_date_str in holidays

            if p_weekday < 5 and not p_is_holiday:
                working_days += 1

            if working_days < 5:
                proj_date += datetime.timedelta(days=1)

            p_days_iterated += 1

        project_date_str = proj_date.strftime("%Y-%m-%d")

        return {
            "end_date": end_date_str,
            "project_date": project_date_str
        }

    def create_batch(
        self,
        batch_code,
        batch_name,
        course_id,
        trainer_id,
        start_date,
        end_date,
        slot_type,
        start_time=None,
        end_time=None,
        mode="Offline",
        location=None,
        max_capacity=30,
        enrolled_count=0,
        status="Upcoming",
        description=None,
        created_by=None
    ):
        """
        Validates input and creates a new batch.
        """
        if not batch_name or not batch_name.strip():
            raise ValueError("Batch Name is required.")

        if not batch_code or not batch_code.strip():
            batch_code = self.generate_batch_code()
        else:
            batch_code = batch_code.strip()

        if self.batch_model.batch_code_exists(batch_code):
            raise ValueError(f"Batch code '{batch_code}' already exists.")

        try:
            course_id = int(course_id)
        except (ValueError, TypeError):
            raise ValueError("Valid Course must be selected.")

        course = self.course_model.get_course_by_id(course_id)
        if not course:
            raise ValueError("Selected course does not exist.")

        if course.get("status") != "Active":
            raise ValueError("Selected course is not active.")

        # Optional Trainer Validation & Conflict Check
        clean_trainer_id = None
        trainer = None
        if trainer_id and str(trainer_id).strip():
            try:
                clean_trainer_id = int(trainer_id)
                t_row = get_trainer_by_id(clean_trainer_id)
                if not t_row:
                    raise ValueError("Selected trainer does not exist.")
                trainer = dict(t_row)
            except (ValueError, TypeError):
                raise ValueError("Invalid trainer ID.")

        if clean_trainer_id and trainer:
            if trainer.get("status") != "Active":
                raise ValueError(f"Assigned trainer '{trainer.get('full_name')}' is Inactive.")

            if not self._check_trainer_skill_alignment(trainer.get("skills"), course.get("technology_stack")):
                raise ValueError(
                    f"Trainer skills ({trainer.get('skills')}) do not align with course technology stack ({course.get('technology_stack')})."
                )

        if not start_date or not end_date:
            raise ValueError("Start date and End date are required.")

        try:
            s_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            e_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Expected YYYY-MM-DD.")

        if s_date > e_date:
            raise ValueError("Start date cannot be after End date.")

        VALID_SLOTS = [
            'Weekday Morning (9:30 AM - 11:30 AM)',
            'Weekday Midday (11:45 AM - 1:45 PM)',
            'Weekday Afternoon (2:45 PM - 4:45 PM)',
            'Weekday Evening (5:00 PM - 7:00 PM)',
            'Weekend Full Day (10:00 AM - 4:00 PM)',
            'Custom'
        ]
        if slot_type not in VALID_SLOTS:
            raise ValueError("Invalid slot type.")

        if mode not in ('Online', 'Offline', 'Hybrid'):
            raise ValueError("Invalid delivery mode.")

        try:
            max_capacity = int(max_capacity)
            if max_capacity <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError("Max capacity must be a positive number.")

        try:
            enrolled_count = int(enrolled_count)
            if enrolled_count < 0:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError("Enrolled count must be zero or a positive number.")

        if enrolled_count > max_capacity:
            raise ValueError("Enrolled count cannot exceed max capacity.")

        VALID_STATUSES = ('Upcoming', 'In Progress', 'Completed', 'On Hold', 'Cancelled')
        if status not in VALID_STATUSES:
            raise ValueError("Invalid batch status.")

        # BR-03 & BR-08: In Progress status requires an assigned trainer and start_date <= today
        if status == 'In Progress':
            if not clean_trainer_id:
                raise ValueError("Trainer assignment is mandatory before setting batch status to 'In Progress'.")
            if s_date > datetime.date.today():
                raise ValueError("Cannot set batch status to 'In Progress' before its start date.")

        # Check Trainer Schedule Conflict
        if clean_trainer_id:
            conflict = self.batch_model.check_trainer_schedule_conflict(
                clean_trainer_id, slot_type, start_date, end_date
            )
            if conflict:
                raise ValueError(
                    f"Trainer scheduling conflict: Assigned trainer is already booked for "
                    f"batch '{conflict['batch_name']}' ({conflict['batch_code']}) in slot '{slot_type}' "
                    f"between {conflict['start_date']} and {conflict['end_date']}."
                )

        new_id = self.batch_model.create_batch(
            batch_code=batch_code,
            batch_name=batch_name.strip(),
            course_id=course_id,
            trainer_id=clean_trainer_id,
            start_date=start_date,
            end_date=end_date,
            slot_type=slot_type,
            start_time=start_time,
            end_time=end_time,
            mode=mode,
            location=location.strip() if location else None,
            max_capacity=max_capacity,
            enrolled_count=enrolled_count,
            status=status,
            description=description.strip() if description else None,
            created_by=created_by
        )

        return {
            "success": True,
            "message": "Batch created successfully.",
            "batch_id": new_id,
            "batch_code": batch_code
        }

    def get_all_batches(self, status=None, course_id=None, trainer_id=None, mode=None, search=None):
        """
        Fetches filtered batch lists.
        """
        return self.batch_model.get_all_batches(
            status=status,
            course_id=course_id,
            trainer_id=trainer_id,
            mode=mode,
            search=search
        )

    def get_batch_by_id(self, batch_id):
        """
        Retrieves a single batch by ID.
        """
        try:
            batch_id = int(batch_id)
        except (ValueError, TypeError):
            raise ValueError("Invalid Batch ID format.")

        batch = self.batch_model.get_batch_by_id(batch_id)
        if not batch:
            raise ValueError(f"Batch with ID {batch_id} not found.")

        return batch

    def update_batch(
        self,
        batch_id,
        batch_name,
        course_id,
        trainer_id,
        start_date,
        end_date,
        slot_type,
        start_time=None,
        end_time=None,
        mode="Offline",
        location=None,
        max_capacity=30,
        status="Upcoming",
        description=None,
        updated_by=None
    ):
        """
        Validates and updates batch details.
        """
        try:
            batch_id = int(batch_id)
        except (ValueError, TypeError):
            raise ValueError("Invalid Batch ID format.")

        existing = self.batch_model.get_batch_by_id(batch_id)
        if not existing:
            raise ValueError("Batch not found.")

        if not batch_name or not batch_name.strip():
            raise ValueError("Batch Name is required.")

        try:
            course_id = int(course_id)
        except (ValueError, TypeError):
            raise ValueError("Valid Course must be selected.")

        course = self.course_model.get_course_by_id(course_id)
        if not course:
            raise ValueError("Selected course does not exist.")

        clean_trainer_id = None
        trainer = None
        if trainer_id and str(trainer_id).strip():
            try:
                clean_trainer_id = int(trainer_id)
                t_row = get_trainer_by_id(clean_trainer_id)
                if not t_row:
                    raise ValueError("Selected trainer does not exist.")
                trainer = dict(t_row)
            except (ValueError, TypeError):
                raise ValueError("Invalid trainer ID.")

        if clean_trainer_id and trainer:
            if trainer.get("status") != "Active":
                raise ValueError(f"Assigned trainer '{trainer.get('full_name')}' is Inactive.")

            if not self._check_trainer_skill_alignment(trainer.get("skills"), course.get("technology_stack")):
                raise ValueError(
                    f"Trainer skills ({trainer.get('skills')}) do not align with course technology stack ({course.get('technology_stack')})."
                )

        if not start_date or not end_date:
            raise ValueError("Start date and End date are required.")

        try:
            s_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            e_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Expected YYYY-MM-DD.")

        if s_date > e_date:
            raise ValueError("Start date cannot be after End date.")

        try:
            max_capacity = int(max_capacity)
            if max_capacity <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError("Max capacity must be a positive number.")

        if existing['enrolled_count'] > max_capacity:
            raise ValueError(f"Max capacity cannot be set lower than currently enrolled students ({existing['enrolled_count']}).")

        # BR-03 & BR-08: In Progress status requires an assigned trainer and start_date <= today
        if status == 'In Progress':
            if not clean_trainer_id:
                raise ValueError("Trainer assignment is mandatory before setting batch status to 'In Progress'.")
            if s_date > datetime.date.today():
                raise ValueError("Cannot set batch status to 'In Progress' before its start date.")

        # Check Trainer Schedule Conflict (excluding current batch)
        if clean_trainer_id:
            conflict = self.batch_model.check_trainer_schedule_conflict(
                clean_trainer_id, slot_type, start_date, end_date, exclude_batch_id=batch_id
            )
            if conflict:
                raise ValueError(
                    f"Trainer scheduling conflict: Assigned trainer is already booked for "
                    f"batch '{conflict['batch_name']}' ({conflict['batch_code']}) in slot '{slot_type}' "
                    f"between {conflict['start_date']} and {conflict['end_date']}."
                )

        success = self.batch_model.update_batch(
            batch_id=batch_id,
            batch_name=batch_name.strip(),
            course_id=course_id,
            trainer_id=clean_trainer_id,
            start_date=start_date,
            end_date=end_date,
            slot_type=slot_type,
            start_time=start_time,
            end_time=end_time,
            mode=mode,
            location=location.strip() if location else None,
            max_capacity=max_capacity,
            status=status,
            description=description.strip() if description else None,
            updated_by=updated_by
        )

        if not success:
            raise ValueError("Failed to update batch details.")

        return {
            "success": True,
            "message": "Batch updated successfully."
        }

    def update_status(self, batch_id, status, updated_by=None):
        """
        Updates batch status with lifecycle validation.
        """
        try:
            batch_id = int(batch_id)
        except (ValueError, TypeError):
            raise ValueError("Invalid Batch ID format.")

        VALID_STATUSES = ('Upcoming', 'In Progress', 'Completed', 'On Hold', 'Cancelled')
        if status not in VALID_STATUSES:
            raise ValueError("Invalid batch status.")

        batch = self.batch_model.get_batch_by_id(batch_id)
        if not batch:
            raise ValueError("Batch not found.")

        # BR-03 & BR-08: In Progress status validation
        if status == 'In Progress':
            if not batch.get('trainer_id'):
                raise ValueError("Trainer assignment is mandatory before setting batch status to 'In Progress'.")
            try:
                s_date = datetime.datetime.strptime(batch['start_date'], "%Y-%m-%d").date()
                if s_date > datetime.date.today():
                    raise ValueError("Cannot set batch status to 'In Progress' before its start date.")
            except ValueError:
                pass

        success = self.batch_model.update_status(batch_id, status, updated_by)
        if not success:
            raise ValueError("Batch status could not be updated.")

        return {
            "success": True,
            "message": f"Batch status updated to '{status}' successfully."
        }

    def delete_batch(self, batch_id):
        """
        Deletes a batch.
        """
        try:
            batch_id = int(batch_id)
        except (ValueError, TypeError):
            raise ValueError("Invalid Batch ID format.")

        existing = self.batch_model.get_batch_by_id(batch_id)
        if not existing:
            raise ValueError("Batch not found.")

        if existing.get("enrolled_count", 0) > 0:
            raise ValueError("Cannot delete a batch with enrolled students.")

        success = self.batch_model.delete_batch(batch_id)
        if not success:
            raise ValueError("Failed to delete batch.")

        return {
            "success": True,
            "message": "Batch deleted successfully."
        }

    def get_statistics(self):
        """
        Returns calculated batch operational metrics.
        """
        return self.batch_model.get_statistics()

