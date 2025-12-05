# Day-1 Deliverable — Step-by-step README

This README explains, step-by-step, how I implemented **Day‑1** deliverables for the ingestion pipeline:
creating the storage account and container layout, enabling Event Grid, creating & deploying the Event Grid → Azure Function (local development → Azure), adding environment variables, creating the ingestion queue in the storage account, and uploading test files to trigger the pipeline.

---

## 1. Create Storage Account (ADLS Gen2 enabled)

1. Under **Advanced** enable **Hierarchical namespace** (this makes it ADLS Gen2).
2. After deployment, open the storage account, create container `raw`.
3. Inside `raw` create directories (virtual folders):
   - `atm/`
   - `upi/`
   - `customers/`
   You can create them in the portal by "Add Directory" inside the `raw` container.

---

## 2. Create Azure Function project locally (Event Grid trigger)

---

## 3. Run & Test Locally

---

## 4. Deploy Event Grid Function to Azure

1. After deployment, go to the Function App → **Configuration** → add application settings:
   - `AzureWebJobsStorage` → storage connection string
   - `QueueConnection` → storage connection string (used by queue output binding)

> **Important**: In production avoid storing secrets in app settings; use Key Vault and managed identity.
---

## 5. Create Storage Queue in the Storage Account
1. Create queue named: `ingestionqueue`.
---

## 6. Configure Event Grid Subscription for specific containers

---

## 7. Upload test files into the container folders

---

## 9. Monitoring & Troubleshooting

- **Function logs**
- **Queue messages**
- **Event Grid**

---

## 10. Result (screenshot)

Below is the screenshot showing messages in the `ingestionqueue` after uploading files to the `raw` container.

<img width="1854" height="878" alt="Screenshot 2025-12-05 115647" src="https://github.com/user-attachments/assets/dde3a834-f5e5-4a4d-931f-5fa8b8210f3a" />


---
