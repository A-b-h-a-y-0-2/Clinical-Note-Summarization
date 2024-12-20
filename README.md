# Clinical-Note-Summarization
This project aims to build a Clinical Note Summarizer using machine learning models to extract and summarize clinical information from electronic health records (EHRs) stored in XML format. The project involves data processing, feature extraction, model training, and deployment to summarize clinical notes for easier analysis and better insights.

## Model Details
- **Model Name**: Bio-BART Summarizer
- **Framework**: Hugging Face Transformers
- **Model Format**: PyTorch
- *further details can be found here : https://arxiv.org/pdf/2204.03905* 
## Dataset Details

### Columns
1. **`paragraphs_cleaned`**: 
    - The cleaned and preprocessed long-form clinical notes or detailed paragraphs.
    - Example: 
      ```
      "Clinical notes often contain verbose and repetitive information, including details about patient history, symptoms, and treatments."
      ```

2. **`abstract_cleaned`**: 
    - The cleaned and preprocessed short-form summaries or abstracts of the clinical notes.
    - Example: 
      ```
      "Clinical notes are verbose and detailed."
      ```

---

## Data Statistics

- **Total Rows**: 30k approx
- **Columns**: 2
  - `paragraphs_cleaned`
  - `abstract_cleaned`

### Data Split
- **Training Set**: (80%)
- **Validation Set**: (10%)
- **Test Set**: (10%)

## Loss Curve
![Training Loss Curve][https://github.com/A-b-h-a-y-0-2/Clinical-Note-Summarization/blob/main/loss%20curve(20%20epochs).png] 
