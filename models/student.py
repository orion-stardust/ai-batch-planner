import sqlite3
from database.db import get_connection

class StudentModel:
    def create_student(self, full_name, email, phone, enrollment_date, status, course_id=None, batch_id=None, created_by="Admin"):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO student (full_name, email, phone, enrollment_date, status, course_id, batch_id, created_by, updated_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (full_name, email, phone, enrollment_date, status, course_id, batch_id, created_by, created_by))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_all_students(self):
        conn = get_connection()
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.student_id, s.full_name, s.email, s.phone, s.enrollment_date, s.status,
                       s.course_id, c.course_name,
                       s.batch_id, b.batch_code, b.batch_name,
                       s.created_at, s.updated_at, s.created_by, s.updated_by
                FROM student s
                LEFT JOIN Course c ON s.course_id = c.id
                LEFT JOIN batch b ON s.batch_id = b.batch_id
                ORDER BY s.enrollment_date DESC
            ''')
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def get_student_by_id(self, student_id):
        conn = get_connection()
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.student_id, s.full_name, s.email, s.phone, s.enrollment_date, s.status,
                       s.course_id, c.course_name,
                       s.batch_id, b.batch_code, b.batch_name,
                       s.created_at, s.updated_at, s.created_by, s.updated_by
                FROM student s
                LEFT JOIN Course c ON s.course_id = c.id
                LEFT JOIN batch b ON s.batch_id = b.batch_id
                WHERE s.student_id = ?
            ''', (student_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def update_student(self, student_id, full_name, email, phone, status, course_id=None, batch_id=None, updated_by="Admin"):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE student
                SET full_name = ?, email = ?, phone = ?, status = ?,
                    course_id = ?, batch_id = ?,
                    updated_at = CURRENT_TIMESTAMP, updated_by = ?
                WHERE student_id = ?
            ''', (full_name, email, phone, status, course_id, batch_id, updated_by, student_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def delete_student(self, student_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM student WHERE student_id = ?', (student_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def student_exists(self, email=None, phone=None, exclude_id=None):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = 'SELECT 1 FROM student WHERE '
            params = []
            conditions = []
            if email:
                conditions.append('email = ?')
                params.append(email)
            if phone:
                conditions.append('phone = ?')
                params.append(phone)
            
            if not conditions:
                return False

            query += '(' + ' OR '.join(conditions) + ')'
            
            if exclude_id:
                query += ' AND student_id != ?'
                params.append(exclude_id)

            cursor.execute(query, params)
            return cursor.fetchone() is not None
        finally:
            conn.close()

    def search_students(self, keyword):
        conn = get_connection()
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            search_pattern = f'%{keyword}%'
            cursor.execute('''
                SELECT s.student_id, s.full_name, s.email, s.phone, s.enrollment_date, s.status,
                       s.course_id, c.course_name, s.batch_id, b.batch_name
                FROM student s
                LEFT JOIN Course c ON s.course_id = c.id
                LEFT JOIN batch b ON s.batch_id = b.batch_id
                WHERE s.full_name LIKE ? OR s.email LIKE ? OR s.phone LIKE ?
                ORDER BY s.enrollment_date DESC
            ''', (search_pattern, search_pattern, search_pattern))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def filter_students(self, status):
        conn = get_db_connection()
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.student_id, s.full_name, s.email, s.phone, s.enrollment_date, s.status,
                       s.course_id, c.course_name, s.batch_id, b.batch_name
                FROM student s
                LEFT JOIN Course c ON s.course_id = c.id
                LEFT JOIN batch b ON s.batch_id = b.batch_id
                WHERE s.status = ?
                ORDER BY s.enrollment_date DESC
            ''', (status,))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def get_students_by_batch(self, batch_id):
        conn = get_connection()
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.student_id, s.full_name, s.email, s.phone, s.enrollment_date, s.status,
                       s.course_id, c.course_name, s.batch_id, b.batch_name
                FROM student s
                LEFT JOIN Course c ON s.course_id = c.id
                LEFT JOIN batch b ON s.batch_id = b.batch_id
                WHERE s.batch_id = ?
                ORDER BY s.enrollment_date DESC
            ''', (batch_id,))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
