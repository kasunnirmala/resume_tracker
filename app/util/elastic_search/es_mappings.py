APPLICATION_MAPPINGS = {
    "properties": {
        "id": {"type": "text"},
        "job_id": {"type": "text"},
        "resume_src": {"type": "text"},
        "cover_letter_src": {"type": "text"},
        "other_details": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
        "summary": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
        "applied_at": {"type": "text"},
        "updated_at": {"type": "text"},
        "created_at": {"type": "text"},
        "job.id": {"type": "text"},
        "job.company_name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
        "job.company_location": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
        "job.job_title": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
        "job.job_posted_date": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
        "job.job_description": {"type": "text", "fields": {"keyword": {"type": "keyword"}}}
    }
}

APPLICATION_VECTOR_MAPPINGS = {
    "properties": {
        "id": {"type": "text"},
        "content": {"type": "text"},
        "embedding": {
            "type": "dense_vector",
            # "dims": 384,
            "index": True,
            "similarity": "cosine"
        },
    }
}
