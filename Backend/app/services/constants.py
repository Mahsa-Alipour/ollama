PROMPT_1 = """You are given resume : ```{resume}```

then based on the given resume extract information about the person 

the output should be markdown code snippet formatted in the following schema, including the leading and trailing "\`\`\`json" and "\`\`\`"

```json

{
    "Contact Information":{
        "Name":string // name of the person
        "Email":string // email of the person
        "Contact":string // contact number of the person
        "Links":array // link of social profiles
        },
    "About Me":string //about the person
    "Skills":array // skills of the person
    "Work Experience":{
        "title":string // title of position working
        "company":string // company name he is working
        "duration":string // duration of working in the company 
    }
    "Education":{
        "course":string // name of the course
        "branch":string // name of the branch he is studying
        "institute":string // name of the institute
    },
    "Certificates":array // certificate name he has acquired
    "Projects":{
        "name":string // name of the project
        "description":string // description about the project
        "link":string // link to its project
    }
    "Achievement":array // rewards, honours etc. received
    "Volunteer":array // volunteering work done
        
}  ```
"""