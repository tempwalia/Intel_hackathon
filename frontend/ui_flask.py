import os
import uuid
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/')
def index():
	return render_template('form.html')

@app.route('/api/submit', methods=['POST'])
def submit_idea():
	data = request.get_json()
	
	# Validate all required fields
	empty_fields = []
	for field in ["title", "description", "problem", "outcome", "language", "approach", "stack", "complexity", "timeline", "manager"]:
		if not data.get(field) or not str(data.get(field)).strip():
			field_name = field.replace("_", " ").title()
			empty_fields.append(field_name)
	
	if not data.get("skills") or len(data.get("skills", [])) == 0:
		empty_fields.append("Required Skills / Roles")
	
	if empty_fields:
		return jsonify({
			"success": False, 
			"message": f"Please fill in the following required fields: {', '.join(empty_fields)}",
			"errors": empty_fields
		}), 400
	
	# Generate ID
	idea_id = str(uuid.uuid4())[:8]
	
	# Create summary data
	summary_data = {
		"id": idea_id,
		"title": data.get("title"),
		"description": data.get("description"),
		"problem": data.get("problem"),
		"outcome": data.get("outcome"),
		"language": data.get("language"),
		"approach": data.get("approach"),
		"stack": data.get("stack"),
		"complexity": data.get("complexity"),
		"boilerplate_enabled": data.get("boilerplate_enabled", False),
		"dev_count": int(data.get("dev_count", 1)),
		"skills": data.get("skills", []),
		"timeline": data.get("timeline"),
		"manager": data.get("manager"),
	}
	
	# Save to JSON file
	record_file = os.path.join(UPLOAD_DIR, f"{idea_id}.json")
	with open(record_file, "w", encoding="utf-8") as f:
		json.dump(summary_data, f, indent=2, ensure_ascii=False)
	
	return jsonify({
		"success": True,
		"id": idea_id,
		"message": "✅ Idea submitted successfully!",
		"data": summary_data,
		"file": record_file
	}), 201

if __name__ == '__main__':
	app.run(debug=True, port=5000)
