const workExperience = [

    {
        company: "LEEDS BECKETT UNIVERSITY",
        role: "SENIOR LECTURER",
        duration: "Jan 2021 - Present",
        description: "Senior module leader for data science programs.\n" +
            "Data science research project supervision and management.\n" +
            "Teaching machine learning and data engineering modules.\n" +
            "Implemented VisWall services, for visual analytics projects.\n" +
            "Providing data driven solutions for university collaborators.\n" +
            "Co-PI in NLP research C- BERT models for fintech start-ups.\n" +
            "Provide Azure data engineering solutions to Morelife."

    },
    {
        company: "Freelancer",
        role: "DATA CONSULTANT",
        duration: "Nov 2020 - Apr 2021",
        description: "Building and maintaining data pipeline to transfer legacy data to Azure cloud.\n" +
            "Collaborate with store managers and analyst to ensure that data is properly formatted\n" +
            "and accessible.\n" +
            "Build analytics tools on azure synapse to utilize legacy data and provide actionable\n" +
            "insights for inventories and sales promotions.\n" +
            "Develop market basket analysis product on POS tractional data to deliver key insights on\n" +
            "sales patterns."
    },
    {
        company: "LIST (LUXEMBOURG INSTITUTE OF SCIENCE &\n" +
            "TECHNOLOGY)",
        role: "DATA SCIENTIST,",
        duration: "Oct 2018 - Nov 2020",
        description: "Engagement with partners and stakeholders for data analytics requirements.\n" +
            "Develop and implement machine learning solutions to reduce production time.\n" +
            "Cross-functional role in project management team to build relationships and explain data\n" +
            "findings to senior stakeholders and members of staffs.\n" +
            "Produced efficient and maintainable code in Python.\n" +
            "Data engineering task on Azure data factory and Data brick, Synapse analytics.\n" +
            "Develop tree-based ensemble of surrogate models in federated learning environment." +
            "Research on transfer learning C-BERT NLP frameworks on Bloomberg data.\n" +
            "Full stack data engineering with Python, SQL, Flask, d3.js , React-java script.\n" +
            "Constantly upgrade knowledgebase with current data science research and technologies"
    },
    {
        company: "Ediburgh Napier University",
        role: "PhD research student",
        duration: "Dec 2014 - July 2018",
        description: "Research on context-aware pervasive computing, IoT data fusion, pattern recognition.\n" +
            "Heterogeneous IoT sensors pre-processing, noise filtering and feature selection.\n" +
            "Develop surrogate models for classification and regression tasks.\n" +
            "Time series data filtering and feature extraction for key events to build probabilistic\n" +
            "model using HMM, NB and RNN."
    },

    {
        company: "Adidas-Group",
        role: "IT engineer",
        duration: "Sep 2007 - Feb 2012",
        description: "Provide ERP Support – Microsoft Dynamics NAV, Ramco, Cognos.\n" +
            "Develop customize financial operations reports using SQL.\n" +
            "Administrate BI tools : Qlik, IBM-Cognos, Crystal Reports.\n" +
            "Database administrator(Backup/Scheduling/Log-Shipping, Performance Tuning)\n" +
            "Create and maintain RPA solution documentation and provide ERP modules training to\n" +
            "business users.\n" +
            "Develop custom financial software's packages(C#.NET, VB, WinForm ADO.NET, SQL) and\n" +
            "conduct user acceptance test(UAT).\n" +
            "IT vendor management and collaboration."
    }
];
const educationExperience = [
    {
        university: "Edinburgh Napier University",
        year : "2014 - 2018",
        thesis: "Conginitive IoE approach to ambient intelligent smart space",
       degree : "PhD in computer science"


    },

    {
        university: "Leeds Beckett University",
        year: "2012 - 2014",
        thesis: "component based software engineering",
        degree : "MSc in Software engineering"

    },

    {
        university: "University of Delhi",
        year : "2007 - 2011",
        degree: "B.Com"
    }
];
function createTimelineItem(experience, isWorkExperience) {
    const item = document.createElement('div');
    item.className = 'timeline-item';

    const date = document.createElement('div');
    date.className = 'timeline-date';
    date.textContent = isWorkExperience ? experience.duration : experience.year;

    const content = document.createElement('div');
    content.className = 'timeline-content';

    if (isWorkExperience) {
        const title = document.createElement('h3');
        title.textContent = `${experience.role} at ${experience.company}`;

        const description = document.createElement('p');
        description.textContent = experience.description;

        content.appendChild(title);
        content.appendChild(description);
    } else {
        const title = document.createElement('h3');
        title.textContent = `${experience.degree} from ${experience.university}`;

        const thesis = document.createElement('p');
        thesis.textContent = `Thesis: ${experience.thesis}`;

        content.appendChild(title);
        content.appendChild(thesis);
    }

    item.appendChild(date);
    item.appendChild(content);
    // Add click event to toggle the expanded class
    item.addEventListener('click', () => {
        content.classList.toggle('expanded');
    });


    return item;
}

function loadTimeline(containerId, experiences, isWorkExperience) {
    const container = document.getElementById(containerId);
    experiences.forEach(exp => {
        const timelineItem = createTimelineItem(exp, isWorkExperience);
        container.appendChild(timelineItem);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    loadTimeline('timeline-container-work', workExperience, true);
    loadTimeline('timeline-container-education', educationExperience, false);
});
