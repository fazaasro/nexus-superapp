---
name: google-cloud-ops
version: 1.0.0
description: |
  Google Cloud Platform (GCP) operations for autonomous agents.
  
  Manage Cloud Storage, Gmail, Calendar, Drive, and Sheets.
  Integates with OpenClaw gateway for seamless automation.

when_to_use:
  - Uploading/downloading files to Google Cloud Storage
  - Sending emails via Gmail API
  - Creating/managing calendar events
  - Managing Google Drive files and folders
  - Manipulating Google Sheets data
  - Listing Google Cloud projects
  - Managing Google Cloud services
  - Authentication with service account
  - Project management

when_not_to_use:
  - Simple cloud storage (use storage-wars-2026 skill instead)
  - Local file operations (use file tool)
  - Non-Google email operations (use other email tools)

tools_involved:
  - gcloud CLI (Google Cloud command line tool)
  - exec (for shell commands and file operations)
  - web_fetch (for Google API interactions)

network_policy: restricted
allowed_domains:
  - googleapis.com
  - www.googleapis.com
  - storage.googleapis.com
  - mail.google.com
  - calendar.google.com
  - docs.google.com
  - sheets.googleapis.com

expected_artifacts:
  - Uploaded files in Google Cloud Storage
  - Sent emails and notifications
  - Created calendar events
  - Updated spreadsheets
  - Authentication tokens
  - Project IDs and configurations

success_criteria:
  - Google APIs authenticated
  - Service account configured
  - Cloud Storage uploads succeed
  - Email notifications sent
  - Calendar events created
  - Drive files uploaded/modified
  - Sheets updated
  - All operations logged

---

## Workflows

### upload_to_gcs

Upload files to Google Cloud Storage.

**Parameters:**
- \`file\`: Path to file to upload
- \`bucket\`: Google Cloud Storage bucket name
- \`destination\`: Target path in bucket (optional)

**Steps:**
1. Verify file exists
2. Upload file to specified bucket
3. Confirm upload success
4. Get file URL for sharing

**Example:**
\`\`\`bash
# Upload file
upload_to_gcs file="/home/ai-dev/data/report.pdf" bucket="aac-backups"

# Output:
✅ File uploaded successfully
📁 URL: https://storage.cloud.google.com/storage/v1/b/aac-backups/o/report.pdf
\`\`\`

---

### send_email

Send email via Gmail API.

**Parameters:**
- \`to\`: Recipient email address
- \`subject\`: Email subject
- \`body\`: Email body (HTML or plain text)
- \`attachment\`: Path to file to attach (optional)

**Steps:**
1. Authenticate with Gmail API
2. Construct email message
3. Send email
4. Verify delivery

**Example:**
\`\`\`bash
# Send notification email
send_email to="fazaasro@gmail.com" subject="VPS Status Update" body="All systems are running smoothly." attachment="/home/ai-dev/reports/status.html"

# Output:
✅ Email sent successfully
📧 Message-ID: 1234567890abcdef
\`\`\`

---

### create_event

Create event in Google Calendar.

**Parameters:**
- \`title\`: Event title
- \`description\`: Event description
- \`start\`: Start time (ISO 8601 or RFC 3339)
- \`end\`: End time (ISO 8601 or RFC 3339)
- \`attendees\`: List of attendee emails (optional)
- \`location\`: Event location (optional)
- \`color\`: Event color (default: blue)

**Steps:**
1. Format start/end times
2. Create event via Gmail Calendar API
3. Verify event created
4. Send notification (optional)

**Example:**
\`\`\`bash
# Create calendar event
create_event title="VPS Status Check" description="Verify all Docker containers and services are running" start="2026-02-15T10:00:00Z" end="2026-02-15T11:00:00Z" attendees="fazaasro@gmail.com,gabriela.servitya@gmail.com" color="blue"

# Output:
✅ Event created successfully
📅 Event ID: 1234567890abcdef
📅 Calendar: primary
\`\`\`

---

### upload_to_drive

Upload files to Google Drive.

**Parameters:**
- \`file\`: Path to file to upload
- \`folder\`: Target folder in Drive (optional)
- \`share\`: Whether to share file (default: false)

**Steps:**
1. Authenticate with Drive API
2. Upload file or folder
3. Set permissions
4. Get shareable link (if share=true)

**Example:**
\`\`\`bash
# Upload to Drive
upload_to_drive file="/home/ai-dev/reports/status.html" folder="aac-vps-reports"

# Output:
✅ File uploaded successfully
📁 File ID: 1A2B3C4D5E6F7G8H9I0J3K6L8M5Q9
📁 Share link: https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9I0J3K6L8M5Q9/view?usp=sharing&usp=drivesdk
\`\`\`

---

### list_projects

List Google Cloud projects.

**Parameters:**
- \`filter\`: Optional filter string

**Steps:**
1. List all projects
2. Show project IDs, names, and numbers
3. Display current project if set

**Example:**
\`\`\`bash
# List projects
list_projects

# Output:
📊 Project ID: project-levy-123456
📋 Project Name: Project Levy
📊 Project Number: 123456789
📋 Current Project: project-levy-123456 (selected)
\`\`\`

---

### create_spreadsheet

Create a new Google Sheet.

**Parameters:**
- \`title\`: Sheet title
- \`rows\`: Initial data rows
- \`columns\`: Column headers

**Steps:**
1. Create spreadsheet
2. Add data rows
3. Format cells
4. Get spreadsheet URL

**Example:**
\`\`\`bash
# Create spreadsheet
create_spreadsheet title="VPS Resource Usage" rows=["Service","Status","Memory","%"] columns=["Service","Status","Memory","%"]

# Output:
✅ Spreadsheet created successfully
📁 Spreadsheet ID: 1A2B3C4D5E6F7G8H9I0J3K6L8M5Q9
📁 URL: https://docs.google.com/spreadsheets/d/1A2B3C4D5E6F7G8H9I0J3K6L8M5Q9/edit
\`\`\`

---

### update_spreadsheet

Update existing Google Sheet.

**Parameters:**
- \`spreadsheet_id\`: Spreadsheet ID
- \`range\`: Cell range to update
- \`values\`: Values to set

**Steps:**
1. Get spreadsheet by ID
2. Identify range
3. Update cells
4. Verify update

**Example:**
\`\`\`bash
# Update spreadsheet
update_spreadsheet spreadsheet_id="1A2B3C4D5E6F7G8H9I0J3K6L8M5Q9" range="Sheet1!A1:C1" values=["Updated: 2026-02-15"]

# Output:
✅ Spreadsheet updated successfully
📁 Range: Sheet1!A1:C1
📁 Updated cells: A1="Updated: 2026-02-15", C1="15"
\`\`\`

---

### add_event_to_sheet

Add event data to existing spreadsheet.

**Parameters:**
- \`spreadsheet_id\`: Spreadsheet ID
- \`sheet_name\`: Sheet name (if not ID)
- \`range\`: Cell range to write
- \`data\`: Array of values

**Steps:**
1. Get spreadsheet
2. Identify range
3. Write event data to range
4. Format cells

**Example:**
\`\`\`bash
# Add event to spreadsheet
add_event_to_sheet spreadsheet_id="1A2B3C4D5E6F7G8H9I0J3K6L8M5Q9" range="Sheet1!A1:C1" data=["Pre-Reunion","Feb 14, 2026","14:00-16:00 WIB"]

# Output:
✅ Event added to spreadsheet
📁 Updated cells: A1="Pre-Reunion", B1="Feb 14, 2026", C1="14:00-16:00 WIB"
\`\`\`

---

### list_events

List calendar events.

**Parameters:**
- \`start\`: Start time (optional)
- \`end\`: End time (optional)
- \`max_results\`: Maximum number of results

**Steps:**
1. Get all events
2. Filter by time range if specified
3. Display events in chronological order
4. Extract relevant information

**Example:**
\`\`\`bash
# List calendar events
list_events start="2026-02-15T00:00:00Z" end="2026-02-15T23:59:59Z" max_results=10

# Output:
📅 1. Pre-Reunion (Feb 14, 2026 14:00:16:00 WIB) — Location: Dreamcourt Grafika Sport Arena
  - Title: ITB "Signum" Alumni Pre-Reunion
  - Start: Feb 14, 2026 at 14:00
  - End: Feb 14, 2026 at 16:00
  - Location: Dreamcourt Grafika Sport Arena
  - Description: Pre-gathering before Dies Natalis

📅 2. Dies Natalis (Feb 21, 2026 15:00-21:00 WIB) — Location: Gedung CRCS, ITB Kampus Ganesha
  - Title: ITB "Signum" Dies Natalis
  - Start: Feb 21, 2026 at 15:00
  - End: Feb 21, 2026 at 21:00
  - Location: Gedung CRCS, ITB Kampus Ganesha
  - Description: 10th Anniversary Gala + Campus Tour

Events:
1. Pre-Reunion
   - Title: ITB "Signum" Alumni Pre-Reunion
   - Start: Feb 14, 2026 at 14:00
   - End: Feb 14, 2026 at 16:00
   - Location: Dreamcourt Grafika Sport Arena
   - Description: Pre-gathering before Dies Natalis

2. Dies Natalis
   - Title: ITB "Signum" Dies Natalis
   - Start: Feb 21, 2026 at 15:00
   - End: Feb 21, 2026 at 21:00
   - Location: Gedung CRCS, ITB Kampus Ganesha
   - Description: 10th Anniversary Gala + Campus Tour
\`\`\`

---

### auth_status

Check current authentication status.

**Parameters:** None

**Steps:**
1. Check gcloud auth list
2. Verify active account
3. Show project configuration
4. Display user information

**Output:**
\`\`\`markdown
# Authentication Status
- Active Account: levy-s@project-levy.iam.gserviceaccount.com
- Project: project-levy
- Configuration: /home/ai-dev/.openclaw/config/gcli
- Credentials: /home/ai-dev/.openclaw/credentials.json
- Environment: Production (service account)

Status: ✅ Fully Authenticated
\`\`\`

---

### configure_gcloud

Configure gcloud settings.

**Parameters:**
- \`account\`: Account to use (default: service account)
- \`project\`: Default project
- \`region\`: Default region
- \`disable_usage_reporting\`: Disable usage reporting

**Steps:**
1. Set active account
2. Set default project
3. Configure region
4. Apply settings
5. Verify configuration

**Example:**
\`\`\`bash
# Configure gcloud
configure_gcloud account="service-account" project="project-levy" region="us-central1" disable_usage_reporting=true

# Output:
✅ Gcloud configured
📊 Account: levy-s@project-levy.iam.gserviceaccount.com
📊 Project: project-levy
📊 Region: us-central1
📊 Usage Reporting: Disabled
\`\`\`

---

## Templates

### email_template

Standard Gmail email template.

\`\`\`html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Subject</title>
</head>
<body>
  <h2>Subject</h2>
  <p>Body</p>
  <p>Attachment: <a href="attachment_url">Download</a></p>
  <hr>
  <p><em>Sent via Levy Google Cloud Ops Skill</em></p>
</body>
</html>
\`\`\`

---

### calendar_event_template

Standard Google Calendar event template.

\`\`\`json
{
  "summary": "VPS Status Check",
  "description": "Verify all Docker containers and services are running",
  "start": {
    "date": "2026-02-15",
    "time": "10:00:00Z"
  },
  "location": {
    "displayName": "Dreamcourt Grafika Sport Arena",
    "location": {
      "title": "Dreamcourt Grafika Sport Arena",
      "address": "Jl. Dreamcourt Graha, No. 123, Jakarta Selatan"
    }
  }
}
\`\`\`

---

### spreadsheet_row_template

Standard Google Sheets row template.

\`\`\`json
{
  "service": "Container",
  "status": "Running",
  "memory": "250MB",
  "cpu": "2.5%",
  "uptime": "30 days"
}
\`\`\`

---

## Guardrails

### Security
- Never expose service account keys
- Use environment variables for credentials
- Validate all inputs (emails, file paths, bucket names)
- Sanitize all external data (URLs, file paths)
- Use least privilege principle

### Data Protection
- Encrypt sensitive data at rest
- Never log credentials or tokens
- Validate file permissions before operations
- Use share permissions carefully for Drive files

### Performance
- Batch operations where possible
- Use compression for large uploads
- Cache results where appropriate
- Use async operations for independent tasks

### Reliability
- Handle API rate limits gracefully
- Retry failed operations with exponential backoff
- Validate all operations before proceeding
- Log all actions for audit trail

### Usability
- Clear progress indicators
- Human-readable error messages
- Color-coded output (✅ success, ⚠️ warning, ❌ error)
- Detailed status updates

### Scalability
- Use pagination for large datasets
- Stream large file uploads
- Process independent tasks in parallel
- Handle rate limits efficiently

### Portability
- Cross-platform compatible commands
- Use standard file paths
- No hardcoded paths or IPs
- Use environment variables for configuration

### Testability
- Each workflow has test strategy
- Validate results before proceeding
- Dry-run mode available
- Comprehensive logging for debugging

### Flexibility
- Modular design (each workflow is independent)
- Easy to extend with new Google Cloud services
- Semantic versioning (1.0.0 → 1.1.0)
- Backwards compatible changes

---

## Negative Examples

### When NOT to use this skill

- Don't use for local file operations (use file tool)
- Don't use for non-Google cloud storage (use storage-wars-2026 skill)
- Don't use for non-Google email operations (use other email tools)

### What to do instead

**Simple file operations:**
\`\`\`bash
# Instead of:
upload_to_gcs file="/home/ai-dev/data/small.txt"

# Do:
file.read path="/home/ai-dev/data/small.txt"
# Then process as needed
\`\`\`

**Email operations:**
\`\`\`bash
# Instead of:
send_email to="user@example.com" subject="Update"

# Do:
# Use system email tool or your existing email infrastructure
\`\`\`

---

## Artifact Locations

All Google Cloud artifacts and logs go to:
- \`workspace/google-cloud/logs/\` — Gcloud CLI operations
- \`workspace/google-cloud/credentials/\` — Authentication files
- \`workspace/google-cloud/config/\` — Configuration files
- \`workspace/google-cloud/projects/\` — Project configurations
- \`workspace/google-cloud/storage/\` — Upload/download logs

---

## Version History

- 1.0.0 — Initial release with Google Cloud Platform integration
  - Gmail, Calendar, Drive, Sheets integration
  - Service account authentication
  - Cloud Storage operations
  - Project management

---

*Google Cloud Platform integration for autonomous agents*
\EOF
