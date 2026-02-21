from pipeline import HRScreeningPipeline

if __name__ == "__main__":
    pipeline = HRScreeningPipeline()

    input_data = {
        "job_description": (
            "We are looking for a Junior QA Engineer with experience in "
            "Python, API testing, and manual testing methodologies."
        ),
        "resume_text": (
            "Worked as a QA intern. Performed manual testing, "
            "used Postman for API checks, and wrote basic Python scripts."
        ),
        "metadata": {
            "candidate_id": "CAND-001",
            "job_id": "JOB-123",
            "source": "linkedin"
        }
    }

    output = pipeline.run(input_data)

    print("\n=== SCREENING RESULT ===")
    print(output["result"])

    print("\n=== EVALUATION ===")
    print(output["evaluation"])
