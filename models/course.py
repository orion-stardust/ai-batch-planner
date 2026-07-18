
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "batch_planner.db")


class CourseModel:

    def get_connection(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    
    def create_course(self, course_name, technology_stack, duration_hours,
                      description, status="Active", created_by=None):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Course(
                course_name,technology_stack,duration_hours,
                description,status,created_by
            ) VALUES(?,?,?,?,?,?)
        """, (course_name, technology_stack, duration_hours,
              description, status, created_by))
        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return new_id

    
    def get_all_courses(self):
        conn = self.get_connection()
        rows = conn.execute("SELECT * FROM Course ORDER BY course_name ASC").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_course_by_id(self, course_id):
        conn = self.get_connection()
        row = conn.execute("SELECT * FROM Course WHERE id=?", (course_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def get_course_by_name(self, course_name):
        conn = self.get_connection()
        row = conn.execute("SELECT * FROM Course WHERE course_name=?", (course_name,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def get_active_courses(self):
        return self.get_courses_by_status("Active")

    def get_inactive_courses(self):
        return self.get_courses_by_status("Inactive")

    def get_courses_by_status(self, status):
        conn = self.get_connection()
        rows = conn.execute("SELECT * FROM Course WHERE status=? ORDER BY course_name",(status,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    
    def update_course(self, course_id, course_name, technology_stack,
                      duration_hours, description, status, updated_by):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
        UPDATE Course
        SET course_name=?,technology_stack=?,duration_hours=?,
            description=?,status=?,updated_at=CURRENT_TIMESTAMP,
            updated_by=?
        WHERE id=?
        """,(course_name,technology_stack,duration_hours,
             description,status,updated_by,course_id))
        conn.commit()
        ok = cur.rowcount>0
        conn.close()
        return ok

    def update_status(self, course_id, status, updated_by):
        conn=self.get_connection()
        cur=conn.cursor()
        cur.execute("""UPDATE Course
                       SET status=?,updated_at=CURRENT_TIMESTAMP,updated_by=?
                       WHERE id=?""",(status,updated_by,course_id))
        conn.commit()
        conn.close()
        return cur.rowcount>0

    def delete_course(self, course_id):
        conn=self.get_connection()
        cur=conn.cursor()
        cur.execute("DELETE FROM Course WHERE id=?",(course_id,))
        conn.commit()
        conn.close()
        return cur.rowcount>0

    def course_exists(self, course_name, exclude_id=None):
        conn=self.get_connection()
        if exclude_id:
            row=conn.execute("SELECT 1 FROM Course WHERE course_name=? AND id<>?",
                             (course_name,exclude_id)).fetchone()
        else:
            row=conn.execute("SELECT 1 FROM Course WHERE course_name=?",
                             (course_name,)).fetchone()
        conn.close()
        return row is not None


    def search_courses(self, keyword):
        like=f"%{keyword}%"
        conn=self.get_connection()
        rows=conn.execute("""
        SELECT * FROM Course
        WHERE course_name LIKE ?
           OR technology_stack LIKE ?
           OR description LIKE ?
        ORDER BY course_name
        """,(like,like,like)).fetchall()
        conn.close()
        return [dict(r) for r in rows]


    def filter_courses(self,status=None,technology=None,min_duration=None,max_duration=None,keyword=None):
        sql="SELECT * FROM Course WHERE 1=1"
        params=[]
        if status:
            sql+=" AND status=?"; params.append(status)
        if technology:
            sql+=" AND technology_stack=?"; params.append(technology)
        if min_duration is not None:
            sql+=" AND duration_hours>=?"; params.append(min_duration)
        if max_duration is not None:
            sql+=" AND duration_hours<=?"; params.append(max_duration)
        if keyword:
            sql+=" AND (course_name LIKE ? OR technology_stack LIKE ? OR description LIKE ?)"
            like = f"%{keyword}%"
            params.extend([like, like, like])
        sql+=" ORDER BY course_name ASC"
        conn=self.get_connection()
        rows=conn.execute(sql,params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def count_courses(self):
        conn=self.get_connection()
        c=conn.execute("SELECT COUNT(*) FROM Course").fetchone()[0]
        conn.close()
        return c

    def get_statistics(self):
        conn=self.get_connection()
        cur=conn.cursor()
        stats={
            "total_courses":cur.execute("SELECT COUNT(*) FROM Course").fetchone()[0],
            "active_courses":cur.execute("SELECT COUNT(*) FROM Course WHERE status='Active'").fetchone()[0],
            "inactive_courses":cur.execute("SELECT COUNT(*) FROM Course WHERE status='Inactive'").fetchone()[0],
            "average_duration":cur.execute("SELECT AVG(duration_hours) FROM Course").fetchone()[0]
        }
        conn.close()
        return stats
