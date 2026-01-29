from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ParsedProblem:
    """Document Parse 결과"""
    raw_text: str
    elements: list = field(default_factory=list)
    has_figure: bool = False


@dataclass
class ExtractedFields:
    """Information Extract 결과"""
    problem_text: str
    conditions: list = field(default_factory=list)
    choices: list = field(default_factory=list)
    points: Optional[int] = None
    answer_type: str = "서술형"
    figure_description: Optional[str] = None


@dataclass
class ConceptInfo:
    """개념 분류 결과"""
    subject: str = "수학"
    chapter: str = ""
    topic: str = ""
    concepts: list = field(default_factory=list)
    difficulty: int = 3
    prerequisites: list = field(default_factory=list)


@dataclass
class SimilarProblem:
    """유사문제"""
    problem: str
    difficulty: int = 3
    variation_type: str = "숫자변형"
    hint: str = ""


@dataclass
class ProblemSolution:
    """문제 풀이"""
    steps: list = field(default_factory=list)
    answer: str = ""
    key_point: str = ""


@dataclass
class SolutionResult:
    """전체 풀이 결과"""
    original: ProblemSolution = field(default_factory=ProblemSolution)
    similars: list = field(default_factory=list)


@dataclass
class ErrorNote:
    """최종 오답노트"""
    title: str = ""
    concept_summary: str = ""
    formula_box: list = field(default_factory=list)
    original_problem: str = ""
    original_solution: ProblemSolution = field(default_factory=ProblemSolution)
    similar_problems: list = field(default_factory=list)
    study_tips: str = ""
    next_topics: list = field(default_factory=list)
