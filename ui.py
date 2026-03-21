import os
import uuid
import json
import streamlit as st

st.set_page_config(page_title="Idea Intake Form", layout="wide")

st.title("Idea Intake Form")
st.write("Use this form to submit a new idea. Fill sections and press Submit.")

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

with st.form(key="idea_form"):
	st.header("Section 1: Idea Overview")
	title = st.text_input("Title *", placeholder="e.g., URL Shortener Application")
	description = st.text_area("Description *", height=120, placeholder="Enter a brief description of your project. What does it do? (e.g., Converts long URLs into short, shareable links.)")
	problem = st.text_area("Problem *", placeholder="Describe the problem your project solves (e.g., Long URLs are hard to share and remember.)")
	outcome = st.text_area("Desired Outcome *", placeholder="What will users achieve? (e.g., Generate short links and track usage easily.)")

	st.header("Section 2: Technical Inputs")
	col1, col2 = st.columns(2)
	with col1:
		language = st.text_input("Language / Primary Tech *", placeholder="e.g., Python")
		approach = st.text_area("Approach / Algorithm *", height=200, placeholder="Explain how the solution works (e.g., Generate a unique code and map it to the original URL.)")
	with col2:
		stack = st.text_area("Recommended Stack / Services *", height=200, placeholder="List technologies used (e.g., Flask, SQLite, HTML, CSS)")
		complexity = st.selectbox("Complexity *", ["Low", "Medium", "High"] )
		boilerplate_enabled = st.checkbox("Enable Boilerplate / Scaffold (optional)")

	st.header("Section 3: Resources & Skills")
	dev_count = st.number_input("Developer count (estimate) *", min_value=1, max_value=100, value=1)
	skills = st.multiselect("Required skills / roles *", ["Frontend", "Backend", "ML", "DevOps", "QA", "Data Engineer", "Product"], default=[])
	timeline = st.text_input("Estimated timeline (e.g. 4 weeks) *", placeholder="e.g., 2–5 days")

	st.header("Section 4: Approval")
	manager = st.text_input("Manager / Approver (email or name) *", placeholder="e.g., Project Guide / Teacher")

	# Validate all required fields
	# all_fields_filled = (
	# 	title.strip() and
	# 	description.strip() and
	# 	problem.strip() and
	# 	outcome.strip() and
	# 	language.strip() and
	# 	approach.strip() and
	# 	stack.strip() and
	# 	complexity and
	# 	dev_count > 0 and
	# 	skills and
	# 	timeline.strip() and
	# 	manager.strip()
	# )

	submitted = st.form_submit_button("Submit Idea")

if submitted:
	# Validate all required fields before processing
	empty_fields = []
	if not title.strip():
		empty_fields.append("Title")
	if not description.strip():
		empty_fields.append("Description")
	if not problem.strip():
		empty_fields.append("Problem")
	if not outcome.strip():
		empty_fields.append("Desired Outcome")
	if not language.strip():
		empty_fields.append("Language / Primary Tech")
	if not approach.strip():
		empty_fields.append("Approach / Algorithm")
	if not stack.strip():
		empty_fields.append("Recommended Stack / Services")
	if not complexity:
		empty_fields.append("Complexity")
	if dev_count <= 0:
		empty_fields.append("Developer count")
	if not skills:
		empty_fields.append("Required skills / roles")
	if not timeline.strip():
		empty_fields.append("Estimated timeline")
	if not manager.strip():
		empty_fields.append("Manager / Approver")

	if empty_fields:
		st.error(f"❌ Please fill in the following required fields:\n\n" + "\n".join([f"• {field}" for field in empty_fields]))
	else:
		idea_id = str(uuid.uuid4())[:8]
		
		summary_data = {
			"id": idea_id,
			"title": title,
			"description": description,
			"problem": problem,
			"outcome": outcome,
			"language": language,
			"approach": approach,
			"stack": stack,
			"complexity": complexity,
			"boilerplate_enabled": boilerplate_enabled,
			"dev_count": int(dev_count),
			"skills": skills,
			"timeline": timeline,
			"manager": manager,
		}

		# Save as JSON file
		record_file = os.path.join(UPLOAD_DIR, f"{idea_id}.json")
		with open(record_file, "w", encoding="utf-8") as f:
			json.dump(summary_data, f, indent=2, ensure_ascii=False)

		# Clear form fields after successful submission
		st.session_state.clear()
		
		st.success(f"Idea submitted — ID: {idea_id}")

		st.subheader("Summary")
		summary_data = {
			"id": idea_id,
			"title": title,
			"description": description,
			"problem": problem,
			"outcome": outcome,
			"language": language,
			"approach": approach,
			"stack": stack,
			"complexity": complexity,
			"boilerplate_enabled": boilerplate_enabled,
			"dev_count": int(dev_count),
			"skills": skills,
			"timeline": timeline,
			"manager": manager,
		}
		st.write(summary_data)

		# Save as JSON file
		record_file = os.path.join(UPLOAD_DIR, f"{idea_id}.json")
		with open(record_file, "w", encoding="utf-8") as f:
			json.dump(summary_data, f, indent=2, ensure_ascii=False)

		st.info(f"Record saved to {record_file}")

		st.markdown("---")
		st.write("You can now copy the summary or assign the idea to your tracking system.")

else:
	st.caption("Fill the form and press Submit. Uploaded files will be saved locally in a `frontend/uploads` folder.")