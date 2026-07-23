import sqlite3
from database.db import get_connection

class StudentRegisterModel:
    def create_registration(self, student_id, course_id, enrollment_date, status, batch_id=None, created_by="Admin"):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO student_register (student_id, course_id, batch_id, enrollment_date, status, created_by, updated_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, course_id, batch_id, enrollment_date, status, created_by, created_by))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_all_registrations(self):
        conn = get_connection()
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT sr.register_id, sr.student_id, s.full_name AS student_name,
                       sr.course_id, c.course_name,
                       sr.batch_id, b.batch_name,
                       sr.enrollment_date, sr.status,
                       sr.created_at, sr.updated_at, sr.created_by, sr.updated_by
                FROM student_register sr
                JOIN student s ON sr.student_id = s.student_id
                JOIN Course c ON sr.course_id = c.id
                LEFT JOIN batch b ON sr.batch_id = b.batch_id
                ORDER BY sr.register_id DESC
            ''')
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def get_registration_by_id(self, register_id):
        conn = get_connection()
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT sr.register_id, sr.student_id, s.full_name AS student_name,
                       sr.course_id, c.course_name,
                       sr.batch_id, b.batch_name,
                       sr.enrollment_date, sr.status,
                       sr.created_at, sr.updated_at, sr.created_by, sr.updated_by
                FROM student_register sr
                JOIN student s ON sr.student_id = s.student_id
                JOIN Course c ON sr.course_id = c.id
                LEFT JOIN batch b ON sr.batch_id = b.batch_id
                WHERE sr.register_id = ?
            ''', (register_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def update_registration(self, register_id, student_id, course_id, enrollment_date, status, batch_id=None, updated_by="Admin"):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE student_register
                SET student_id = ?, course_id = ?, batch_id = ?, enrollment_date = ?, status = ?,
                    updated_at = CURRENT_TIMESTAMP, updated_by = ?
                WHERE register_id = ?
            ''', (student_id, course_id, batch_id, enrollment_date, status, updated_by, register_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def delete_registration(self, register_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM student_register WHERE register_id = ?', (register_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def search_registrations(self, keyword):
        conn = get_connection()
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            search_pattern = f'%{keyword}%'
            cursor.execute('''
                SELECT sr.register_id, sr.student_id, s.full_name AS student_name,
                       sr.course_id, c.course_name,
                       sr.batch_id, b.batch_name,
                       sr.enrollment_date, sr.status
                FROM student_register sr
                JOIN student s ON sr.student_id = s.student_id
                JOIN Course c ON sr.course_id = c.id
                LEFT JOIN batch b ON sr.batch_id = b.batch_id
                WHERE s.full_name LIKE ? OR c.course_name LIKE ? OR b.batch_name LIKE ? OR sr.status LIKE ?
                ORDER BY sr.register_id DESC
            ''', (search_pattern, search_pattern, search_pattern, search_pattern))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def get_registrations_by_student(self, student_id):
        conn = get_connection()
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT sr.register_id, sr.student_id, sr.course_id, sr.batch_id, sr.status
                FROM student_register sr
                WHERE sr.student_id = ?
            ''', (student_id,))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
