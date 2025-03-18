## Overview

The Reddit Analyzer frontend is fully compatible with a Python Flask backend. The application allows users to analyze Reddit discussions by specifying subreddits, keywords, and time ranges. This document outlines all API endpoints required for seamless integration between the Next.js frontend and a Flask backend.

## API Endpoints

### 1. API Key Verification

#### `POST /api/verify`

Verifies the validity of Reddit and OpenAI API keys.

**Request:**

```json
{
  "type": "reddit|openai",
  "key": "api_key_string"
}
```

**Response:**

- Status: 200 OK


```json
{
  "success": true,
  "message": "API key verified successfully"
}
```

- Status: 400 Bad Request


```json
{
  "success": false,
  "message": "Invalid API key format"
}
```

**Notes:**

- The frontend expects validation of key format (Reddit keys should start with "praw_" and be at least 20 characters; OpenAI keys should start with "sk-" and be 51 characters)
- The backend should attempt to make a test API call to verify the key works


### 2. Analysis Initiation

#### `POST /api/analyze`

Starts a new Reddit analysis task.

**Request:**

```json
{
  "subreddits": ["technology", "programming"],
  "timeRange": "7d",
  "keywords": ["AI", "machine learning"]
}
```

**Response:**

- Status: 200 OK


```json
{
  "success": true,
  "taskId": "1697385600000",
  "message": "Analysis task started successfully"
}
```

- Status: 400 Bad Request


```json
{
  "success": false,
  "message": "Missing required parameters"
}
```

**Notes:**

- `timeRange` values: "1d" (24 hours), "7d" (week), "30d" (month), "90d" (3 months), "365d" (year)
- The backend should generate a unique `taskId` for tracking the analysis task
- The frontend stores task metadata locally but expects the backend to perform the actual analysis


### 3. Analysis Results

#### `GET /api/analysis/{taskId}`

Retrieves the results of a completed analysis task.

**Response:**

- Status: 200 OK


```json
{
  "status": "completed|pending|failed",
  "data": {
    "keywordData": [
      { "text": "Artificial Intelligence", "value": 64 },
      { "text": "Machine Learning", "value": 42 },
      { "text": "Neural Networks", "value": 31 }
    ],
    "sentimentData": {
      "positive": 45,
      "neutral": 35,
      "negative": 20
    },
    "topPosts": [
      {
        "id": "post1",
        "title": "The future of AI in everyday applications",
        "url": "https://reddit.com/r/technology/post1",
        "score": 1245,
        "comments": 89,
        "sentiment": "positive"
      }
    ],
    "summary": "The Reddit community has shown significant interest in AI technologies over the analyzed period..."
  }
}
```

- Status: 404 Not Found


```json
{
  "success": false,
  "message": "Analysis task not found"
}
```

**Notes:**

- The frontend expects the backend to maintain the state of analysis tasks
- The response should include keyword frequency data, sentiment analysis, top posts, and a summary
- For pending tasks, only the status field is required


### 4. Analysis History

#### `GET /api/history`

Retrieves the user's analysis history.

**Response:**

- Status: 200 OK


```json
[
  {
    "id": "1697385600000",
    "date": "2023-10-15T12:00:00Z",
    "subreddits": ["technology"],
    "keywords": ["AI", "machine learning"],
    "timeRange": "7d",
    "status": "completed"
  },
  {
    "id": "1697299200000",
    "date": "2023-10-14T12:00:00Z",
    "subreddits": ["programming"],
    "keywords": ["Python"],
    "timeRange": "30d",
    "status": "completed"
  }
]
```

**Notes:**

- The frontend displays the most recent analyses first
- The backend should store and retrieve analysis history for the authenticated user


## Data Structures

### Analysis Parameters

```typescript
interface AnalysisParams {
  subreddits: string[];  // Array of subreddit names without "r/" prefix
  timeRange: string;     // "1d", "7d", "30d", "90d", or "365d"
  keywords: string[];    // Array of keywords to analyze
}
```

### Analysis Task

```typescript
interface AnalysisTask {
  id: string;                  // Unique identifier
  date: string;                // ISO timestamp
  subreddits: string[];        // Array of subreddit names
  keywords: string[];          // Array of keywords
  timeRange: string;           // Time range code
  status: "pending"|"completed"|"failed";  // Task status
}
```

### Analysis Results

```typescript
interface AnalysisResults {
  keywordData: {
    text: string;   // Keyword or phrase
    value: number;  // Frequency or relevance score
  }[];
  sentimentData: {
    positive: number;  // Percentage (0-100)
    neutral: number;   // Percentage (0-100)
    negative: number;  // Percentage (0-100)
  };
  topPosts: {
    id: string;           // Post identifier
    title: string;        // Post title
    url: string;          // URL to the Reddit post
    score: number;        // Upvote score
    comments: number;     // Number of comments
    sentiment: string;    // "positive", "neutral", or "negative"
  }[];
  summary: string;        // Text summary of the analysis
}
```

## Authentication Requirements

The frontend currently stores API keys locally and sends them for verification. For a production implementation, consider:

1. Implementing user authentication (JWT or session-based)
2. Storing API keys securely on the backend
3. Adding rate limiting and request validation


## Implementation Notes for Flask Backend

### Basic Flask Structure

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import praw
import openai
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# API key verification endpoint
@app.route('/api/verify', methods=['POST'])
def verify_api_key():
    data = request.json
    key_type = data.get('type')
    key = data.get('key')
    
    # Implement verification logic
    # ...
    
    return jsonify({"success": True, "message": f"{key_type.upper()} API key verified successfully"})

# Analysis endpoint
@app.route('/api/analyze', methods=['POST'])
def start_analysis():
    data = request.json
    subreddits = data.get('subreddits', [])
    time_range = data.get('timeRange')
    keywords = data.get('keywords', [])
    
    # Validate parameters
    if not subreddits or not keywords or not time_range:
        return jsonify({"success": False, "message": "Missing required parameters"}), 400
    
    # Generate task ID and start analysis process
    task_id = str(int(time.time() * 1000))
    
    # Start analysis in background (using Celery or similar)
    # ...
    
    return jsonify({
        "success": True,
        "taskId": task_id,
        "message": "Analysis task started successfully"
    })

# Results endpoint
@app.route('/api/analysis/<task_id>', methods=['GET'])
def get_analysis_results(task_id):
    # Retrieve analysis results for the given task ID
    # ...
    
    return jsonify({
        "status": "completed",
        "data": {
            # Analysis results
        }
    })

# History endpoint
@app.route('/api/history', methods=['GET'])
def get_analysis_history():
    # Retrieve analysis history
    # ...
    
    return jsonify([
        # Analysis history items
    ])

if __name__ == '__main__':
    app.run(debug=True)
```

### Required Python Packages

- Flask: Web framework
- Flask-CORS: Cross-origin resource sharing
- PRAW: Python Reddit API Wrapper
- OpenAI: OpenAI API client
- Pandas: Data analysis
- NLTK or TextBlob: Sentiment analysis
- Celery (optional): Background task processing


## Conclusion

The Reddit Analyzer frontend is designed to work with a RESTful API backend and can be seamlessly integrated with a Flask application. The frontend handles user interface, parameter collection, and result visualization, while the backend is responsible for API key verification, data retrieval from Reddit, analysis processing, and result storage.

By implementing the endpoints described in this document with the specified request and response formats, a Flask backend can fully support the functionality required by the frontend application.

Please make sure to add the following environment variable to your project:

NEXT_PUBLIC_API_BASE_URL Submit