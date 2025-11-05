from typing import Dict, List, Optional
import uuid

# --- Exceptions personnalisées ---
class SchoolError(Exception):
    pass

class CapacityError(SchoolError):
    pass

class DuplicateError(SchoolError):
    pass

# --- Classes de base ---
class Person:
    def __init__(self, nom: str, prenom: str, ident: Optional[str] = None):
        self.nom = nom
        self.prenom = prenom
        self.id = ident or str(uuid.uuid4())

    def fullname(self) -> str:
        return f"{self.prenom} {self.nom}"

    def to_dict(self) -> Dict:
        return {"nom": self.nom, "prenom": self.prenom, "id": self.id}

    def __repr__(self):
        return f"{self.__class__.__name__}({self.fullname()!r}, id={self.id!r})"


class Student(Person):
    def __init__(self, nom: str, prenom: str, ident: Optional[str] = None):
        super().__init__(nom, prenom, ident)
        self._grades: Dict[str, List[float]] = {}  # code_cours -> liste de notes

    def add_grade(self, code_cours: str, note: float):
        if not (0 <= note <= 20):
            raise ValueError("La note doit être entre 0 et 20.")
        self._grades.setdefault(code_cours, []).append(float(note))

    def average(self, code_cours: Optional[str] = None) -> float:
        if code_cours:
            notes = self._grades.get(code_cours, [])
            return sum(notes) / len(notes) if notes else 0.0
        # moyenne générale pondérée uniformément
        all_notes = [n for notes in self._grades.values() for n in notes]
        return sum(all_notes) / len(all_notes) if all_notes else 0.0

    def to_dict(self) -> Dict:
        d = super().to_dict()
        d.update({"grades": self._grades})
        return d


class Teacher(Person):
    def __init__(self, nom: str, prenom: str, specialite: str = "", ident: Optional[str] = None):
        super().__init__(nom, prenom, ident)
        self.specialite = specialite

    def to_dict(self) -> Dict:
        d = super().to_dict()
        d.update({"specialite": self.specialite})
        return d


class Course:
    def __init__(self, nom: str, code: str, teacher: Optional[Teacher] = None, capacity: int = 30):
        self.nom = nom
        self.code = code
        self.teacher = teacher
        self.capacity = max(1, int(capacity))
        self._enrolled: List[Student] = []

    @property
    def enrolled(self) -> List[Student]:
        return list(self._enrolled)

    def enroll(self, student: Student):
        if student in self._enrolled:
            raise DuplicateError(f"Étudiant {student.id} déjà inscrit au cours {self.code}.")
        if len(self._enrolled) >= self.capacity:
            raise CapacityError(f"Capacité atteinte pour le cours {self.code}.")
        self._enrolled.append(student)

    def unenroll(self, student: Student):
        if student in self._enrolled:
            self._enrolled.remove(student)

    def average(self) -> float:
        all_notes = []
        for s in self._enrolled:
            notes = s._grades.get(self.code, [])
            all_notes.extend(notes)
        return sum(all_notes) / len(all_notes) if all_notes else 0.0

    def to_dict(self) -> Dict:
        return {
            "nom": self.nom,
            "code": self.code,
            "teacher_id": self.teacher.id if self.teacher else None,
            "capacity": self.capacity,
            "enrolled_ids": [s.id for s in self._enrolled],
        }

    def __repr__(self):
        return f"Course({self.code!r}, {self.nom!r}, teacher={getattr(self.teacher,'id',None)!r}, enrolled={len(self._enrolled)})"


class School:
    def __init__(self, nom: str):
        self.nom = nom
        self._students: Dict[str, Student] = {}
        self._teachers: Dict[str, Teacher] = {}
        self._courses: Dict[str, Course] = {}

    # -- gestion des personnes --
    def add_student(self, student: Student):
        if student.id in self._students:
            raise DuplicateError(f"Étudiant avec id {student.id} existe déjà.")
        self._students[student.id] = student

    def add_teacher(self, teacher: Teacher):
        if teacher.id in self._teachers:
            raise DuplicateError(f"Enseignant avec id {teacher.id} existe déjà.")
        self._teachers[teacher.id] = teacher

    def find_student(self, ident: str) -> Optional[Student]:
        return self._students.get(ident)

    def find_teacher(self, ident: str) -> Optional[Teacher]:
        return self._teachers.get(ident)

    # -- gestion des cours --
    def create_course(self, nom: str, code: str, teacher_id: Optional[str] = None, capacity: int = 30) -> Course:
        if code in self._courses:
            raise DuplicateError(f"Cours avec code {code} existe déjà.")
        teacher = self._teachers.get(teacher_id) if teacher_id else None
        course = Course(nom, code, teacher, capacity)
        self._courses[code] = course
        return course

    def enroll_student(self, course_code: str, student_id: str):
        course = self._courses.get(course_code)
        if not course:
            raise KeyError(f"Cours {course_code} introuvable.")
        student = self._students.get(student_id)
        if not student:
            raise KeyError(f"Étudiant {student_id} introuvable.")
        course.enroll(student)

    def assign_grade(self, course_code: str, student_id: str, note: float):
        student = self._students.get(student_id)
        if not student:
            raise KeyError(f"Étudiant {student_id} introuvable.")
        if course_code not in self._courses:
            raise KeyError(f"Cours {course_code} introuvable.")
        student.add_grade(course_code, note)

    # -- rapports --
    def course_average(self, course_code: str) -> float:
        course = self._courses.get(course_code)
        if not course:
            raise KeyError(f"Cours {course_code} introuvable.")
        return course.average()

    def student_average(self, student_id: str) -> float:
        student = self._students.get(student_id)
        if not student:
            raise KeyError(f"Étudiant {student_id} introuvable.")
        return student.average()

    def top_students(self, n: int = 3) -> List[Student]:
        ranked = sorted(self._students.values(), key=lambda s: s.average(), reverse=True)
        return ranked[:n]

    # -- sérialisation minimale --
    def to_dict(self) -> Dict:
        return {
            "nom": self.nom,
            "students": [s.to_dict() for s in self._students.values()],
            "teachers": [t.to_dict() for t in self._teachers.values()],
            "courses": {code: c.to_dict() for code, c in self._courses.items()},
        }

    @classmethod
    def sample_school(cls) -> "School":
        sch = cls("Lycée Exemple")
        # créer enseignants
        t1 = Teacher("Dupont", "Alice", specialite="Mathématiques")
        t2 = Teacher("Martin", "Paul", specialite="Physique")
        sch.add_teacher(t1); sch.add_teacher(t2)  # noqa: E702
        # créer étudiants
        s1 = Student("Bernard", "Luc")
        s2 = Student("Moreau", "Emma")
        s3 = Student("Petit", "Noah")
        for s in (s1, s2, s3):
            sch.add_student(s)
        # créer cours et inscriptions
        c1 = sch.create_course("Algèbre", "MATH101", teacher_id=t1.id, capacity=2)
        c2 = sch.create_course("Physique I", "PHY101", teacher_id=t2.id, capacity=30)
        sch.enroll_student("MATH101", s1.id)
        sch.enroll_student("MATH101", s2.id)
        try:
            sch.enroll_student("MATH101", s3.id)  # devrait lever CapacityError
        except CapacityError:
            pass
        sch.enroll_student("PHY101", s1.id)
        sch.enroll_student("PHY101", s2.id)
        sch.enroll_student("PHY101", s3.id)
        # assigner quelques notes
        sch.assign_grade("MATH101", s1.id, 15.5)
        sch.assign_grade("MATH101", s2.id, 12.0)
        sch.assign_grade("PHY101", s1.id, 14.0)
        sch.assign_grade("PHY101", s2.id, 16.0)
        sch.assign_grade("PHY101", s3.id, 13.0)
        return sch

    def __repr__(self):
        return f"School({self.nom!r}, students={len(self._students)}, teachers={len(self._teachers)}, courses={len(self._courses)})"


# --- Démonstration minimale ---
if __name__ == "__main__":
    sch = School.sample_school()
    print(sch)
    # afficher moyennes
    for student in list(sch._students.values()):
        print(f"{student.fullname()} - Moyenne générale: {student.average():.2f}")
    print("Top étudiants:", sch.top_students(2))
    print("Moyenne MATH101:", sch.course_average("MATH101"))
