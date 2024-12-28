
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class ContactInformation(BaseModel):
    Name: str
    Email: EmailStr
    Contact: Optional[str] = None
    Links: Optional[List[str]] = []

class WorkExperienceItem(BaseModel):
    title: str
    company: str
    duration: str

class EducationItem(BaseModel):
    course: str
    branch: str
    institute: str

class ProjectItem(BaseModel):
    name: str
    description: str
    link: str

class VolunteerItem(BaseModel):
    name: str
    description: str

class ReferenceItem(BaseModel):
    name: str
    title: str
    institute: str
    email: EmailStr

class AdditionalInformation(BaseModel):
    remarkable_course_scores: Optional[str] = None
    languages: Optional[List[str]] = []
    interests_hobbies: Optional[str] = None

class ResumeSummary(BaseModel):
    Contact_Information: ContactInformation
    About_Me: str
    Skills: List[str]
    Work_Experience: List[WorkExperienceItem]
    Education: List[EducationItem]
    Certificates: List[str]
    Projects: List[ProjectItem]
    Achievement: List[str]
    Volunteer: List[VolunteerItem]
    Professional_Associations_Volunteer_Activities: Optional[List[dict]] = []
    References: List[ReferenceItem]
    Additional_Information: Optional[AdditionalInformation] = None