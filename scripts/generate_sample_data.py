import os
import numpy as np
import pandas as pd
from pathlib import Path

def generate_student_dataset(num_students=250, seed=42):
    np.random.seed(seed)
    
    student_ids = [f"STU{i:03d}" for i in range(1, num_students + 1)]
    
    # Generate latent overall academic performance factor (0 to 1)
    academic_latent = np.random.beta(a=3, b=2, size=num_students)
    effort_latent = np.random.beta(a=2, b=2, size=num_students)
    
    attendance = np.clip(academic_latent * 50 + effort_latent * 45 + np.random.normal(0, 5, num_students), 30, 100)
    assignments = np.clip(academic_latent * 60 + effort_latent * 35 + np.random.normal(0, 5, num_students), 35, 100)
    internal_marks = np.clip(academic_latent * 65 + effort_latent * 30 + np.random.normal(0, 6, num_students), 30, 100)
    exam_avg = np.clip(academic_latent * 75 + effort_latent * 20 + np.random.normal(0, 7, num_students), 25, 100)
    study_hours = np.clip(effort_latent * 25 + academic_latent * 10 + np.random.normal(0, 2, num_students), 2, 35)
    participation = np.clip(effort_latent * 50 + academic_latent * 45 + np.random.normal(0, 6, num_students), 20, 100)
    prev_sem = np.clip(academic_latent * 70 + effort_latent * 25 + np.random.normal(0, 5, num_students), 35, 100)
    
    # Combined score calculation to determine ground truth risk_level
    composite_score = (
        0.25 * exam_avg +
        0.20 * attendance +
        0.15 * internal_marks +
        0.15 * assignments +
        0.10 * prev_sem +
        0.10 * (study_hours / 35.0 * 100.0) +
        0.05 * participation
    )
    
    risk_level = []
    for score in composite_score:
        if score >= 72.0:
            risk_level.append("Low")
        elif score >= 54.0:
            risk_level.append("Medium")
        else:
            risk_level.append("High")
            
    df = pd.DataFrame({
        "student_id": student_ids,
        "attendance_percentage": np.round(attendance, 1),
        "assignment_average": np.round(assignments, 1),
        "internal_marks": np.round(internal_marks, 1),
        "exam_average": np.round(exam_avg, 1),
        "study_hours_per_week": np.round(study_hours, 1),
        "participation_score": np.round(participation, 1),
        "previous_semester_score": np.round(prev_sem, 1),
        "risk_level": risk_level
    })
    
    return df

if __name__ == "__main__":
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)
    df = generate_student_dataset(250)
    df.to_csv(out_dir / "student_data.csv", index=False)
    print(f"Generated dataset with {len(df)} rows at {out_dir / 'student_data.csv'}")
    print("Risk distribution:")
    print(df["risk_level"].value_counts())
