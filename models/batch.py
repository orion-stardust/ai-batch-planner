import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "batch_planner.db")


class BatchModel:

    def get_connection(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def create_batch(self, batch_code, batch_name, course_id, trainer_id,
                     start_date, end_date, slot_type, start_time=None, end_time=None,
                     mode="Offline", location=None, max_capacity=30, enrolled_count=0,
                     status="Upcoming", description=None, created_by=None):
        """
        Inserts a new batch record into the database.
        Returns the auto-generated batch_id.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO batch (
                batch_code, batch_name, course_id, trainer_id,
                start_date, end_date, slot_type, start_time, end_time,
                mode, location, max_capacity, enrolled_count, status,
                description, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (batch_code, batch_name, course_id, trainer_id,
              start_date, end_date, slot_type, start_time, end_time,
              mode, location, max_capacity, enrolled_count, status,
              description, created_by))
        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return new_id

    def get_all_batches(self, status=None, course_id=None, trainer_id=None, mode=None, search=None):
        """
        Fetches all batches joined with Course and Trainer data, with optional filters.
        """
        sql = """
            SELECT 
                b.*,
                c.course_name,
                c.technology_stack,
                c.duration_hours AS course_duration,
                t.full_name AS trainer_name,
                t.email AS trainer_email,
                t.skills AS trainer_skills
            FROM batch b
            LEFT JOIN Course c ON b.course_id = c.id
            LEFT JOIN trainer t ON b.trainer_id = t.trainer_id
            WHERE 1=1
        """
        params = []

        if status:
            sql += " AND b.status = ?"
            params.append(status)

        if course_id:
            sql += " AND b.course_id = ?"
            params.append(course_id)

        if trainer_id:
            sql += " AND b.trainer_id = ?"
            params.append(trainer_id)

        if mode:
            sql += " AND b.mode = ?"
            params.append(mode)

        if search:
            like = f"%{search}%"
            sql += " AND (b.batch_code LIKE ? OR b.batch_name LIKE ? OR c.course_name LIKE ? OR t.full_name LIKE ?)"
            params.extend([like, like, like, like])

        sql += " ORDER BY b.batch_id DESC"

        conn = self.get_connection()
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_batch_by_id(self, batch_id):
        """
        Retrieves a single batch by batch_id enriched with Course and Trainer data.
        """
        sql = """
            SELECT 
                b.*,
                c.course_name,
                c.technology_stack,
                c.duration_hours AS course_duration,
                t.full_name AS trainer_name,
                t.email AS trainer_email,
                t.skills AS trainer_skills
            FROM batch b
            LEFT JOIN Course c ON b.course_id = c.id
            LEFT JOIN trainer t ON b.trainer_id = t.trainer_id
            WHERE b.batch_id = ?
        """
        conn = self.get_connection()
        row = conn.execute(sql, (batch_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def get_batch_by_code(self, batch_code):
        """
        Retrieves a batch record by unique batch_code.
        """
        conn = self.get_connection()
        row = conn.execute("SELECT * FROM batch WHERE batch_code = ?", (batch_code,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def batch_code_exists(self, batch_code, exclude_id=None):
        """
        Checks if a batch code already exists in the system.
        """
        conn = self.get_connection()
        if exclude_id:
            row = conn.execute("SELECT 1 FROM batch WHERE batch_code = ? AND batch_id <> ?", (batch_code, exclude_id)).fetchone()
        else:
            row = conn.execute("SELECT 1 FROM batch WHERE batch_code = ?", (batch_code,)).fetchone()
        conn.close()
        return row is not None

    def update_batch(self, batch_id, batch_name, course_id, trainer_id,
                     start_date, end_date, slot_type, start_time, end_time,
                     mode, location, max_capacity, status, description, updated_by):
        """
        Updates batch details and refreshes updated_at timestamp.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE batch
            SET batch_name = ?,
                course_id = ?,
                trainer_id = ?,
                start_date = ?,
                end_date = ?,
                slot_type = ?,
                start_time = ?,
                end_time = ?,
                mode = ?,
                location = ?,
                max_capacity = ?,
                status = ?,
                description = ?,
                updated_at = CURRENT_TIMESTAMP,
                updated_by = ?
            WHERE batch_id = ?
        """, (batch_name, course_id, trainer_id, start_date, end_date,
              slot_type, start_time, end_time, mode, location,
              max_capacity, status, description, updated_by, batch_id))
        conn.commit()
        ok = cur.rowcount > 0
        conn.close()
        return ok

    def update_status(self, batch_id, status, updated_by=None):
        """
        Updates the batch status.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE batch
            SET status = ?,
                updated_at = CURRENT_TIMESTAMP,
                updated_by = ?
            WHERE batch_id = ?
        """, (status, updated_by, batch_id))
        conn.commit()
        ok = cur.rowcount > 0
        conn.close()
        return ok

    def delete_batch(self, batch_id):
        """
        Deletes a batch record from the database.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM batch WHERE batch_id = ?", (batch_id,))
        conn.commit()
        ok = cur.rowcount > 0
        conn.close()
        return ok

    def increment_enrolled_count(self, batch_id):
        """
        Increments enrolled_count by 1.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE batch
            SET enrolled_count = enrolled_count + 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE batch_id = ? AND enrolled_count < max_capacity
        """, (batch_id,))
        conn.commit()
        ok = cur.rowcount > 0
        conn.close()
        return ok

    def decrement_enrolled_count(self, batch_id):
        """
        Decrements enrolled_count by 1.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE batch
            SET enrolled_count = enrolled_count - 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE batch_id = ? AND enrolled_count > 0
        """, (batch_id,))
        conn.commit()
        ok = cur.rowcount > 0
        conn.close()
        return ok

    def check_trainer_schedule_conflict(self, trainer_id, slot_type, start_date, end_date, exclude_batch_id=None):
        """
        Checks if a trainer already has an active or upcoming batch in the same slot_type during overlapping dates.
        Returns matching overlapping batch if conflict exists, otherwise None.
        """
        if not trainer_id:
            return None

        sql = """
            SELECT * FROM batch
            WHERE trainer_id = ?
              AND slot_type = ?
              AND status IN ('Upcoming', 'In Progress')
              AND (
                  (start_date <= ? AND end_date >= ?) OR
                  (start_date <= ? AND end_date >= ?) OR
                  (start_date >= ? AND end_date <= ?)
              )
        """
        params = [trainer_id, slot_type, start_date, start_date, end_date, end_date, start_date, end_date]

        if exclude_batch_id:
            sql += " AND batch_id <> ?"
            params.append(exclude_batch_id)

        conn = self.get_connection()
        row = conn.execute(sql, params).fetchone()
        conn.close()
        return dict(row) if row else None

    def get_statistics(self):
        """
        Computes overall operational statistics for dashboard widgets.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        
        total = cur.execute("SELECT COUNT(*) FROM batch").fetchone()[0] or 0
        active = cur.execute("SELECT COUNT(*) FROM batch WHERE status = 'In Progress'").fetchone()[0] or 0
        upcoming = cur.execute("SELECT COUNT(*) FROM batch WHERE status = 'Upcoming'").fetchone()[0] or 0
        completed = cur.execute("SELECT COUNT(*) FROM batch WHERE status = 'Completed'").fetchone()[0] or 0
        on_hold = cur.execute("SELECT COUNT(*) FROM batch WHERE status = 'On Hold'").fetchone()[0] or 0
        cancelled = cur.execute("SELECT COUNT(*) FROM batch WHERE status = 'Cancelled'").fetchone()[0] or 0
        
        enrolled_sum = cur.execute("SELECT SUM(enrolled_count) FROM batch").fetchone()[0] or 0
        capacity_sum = cur.execute("SELECT SUM(max_capacity) FROM batch").fetchone()[0] or 0
        
        utilization = round((enrolled_sum / capacity_sum * 100), 1) if capacity_sum > 0 else 0.0

        conn.close()
        return {
            "total_batches": total,
            "active_batches": active,
            "upcoming_batches": upcoming,
            "completed_batches": completed,
            "on_hold_batches": on_hold,
            "cancelled_batches": cancelled,
            "total_students_enrolled": enrolled_sum,
            "total_capacity": capacity_sum,
            "capacity_utilization": utilization
        }
