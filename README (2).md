# Day-1 Deliverable — Step-by-step README

This README explains, step-by-step, how I implemented **Day‑1** deliverables for the ingestion pipeline:
creating the storage account and container layout, enabling Event Grid, creating & deploying the Event Grid → Azure Function (local development → Azure), adding environment variables, creating the ingestion queue in the storage account, and uploading test files to trigger the pipeline.

---

## 1. Create Storage Account (ADLS Gen2 enabled)

1. In Azure Portal → **Storage accounts** → **+ Create**.
2. Choose **Resource group**, **Name** (e.g. `partheevstorage`), **Region**, **Performance: Standard**, **Account kind: StorageV2 (general purpose v2)**.
3. Under **Advanced** enable **Hierarchical namespace** (this makes it ADLS Gen2).
4. Review + Create.
5. After deployment, open the storage account → **Containers** → **+ Container** and create container `raw`.
6. Inside `raw` create directories (virtual folders):
   - `atm/`
   - `upi/`
   - `customers/`
   You can create them in the portal by "Add Directory" inside the `raw` container.

---

## 2. Configure Event Grid Subscription for specific containers

1. Go to your storage account → **Events** (or Event Grid → Event Subscriptions).
2. Click **+ Event Subscription**.
3. Name the subscription (e.g. `blob-created-to-func`).
4. In **Event Types** choose **Blob created** (and optionally Blob deleted).
5. **Scope / Topic**: ensure it uses the storage account (system topic).
6. **Filter**: Use the **Subject begins with** or advanced filters to restrict to a specific folder:
   - e.g. `"/blobServices/default/containers/raw/blobs/atm/"` or use the portal file picker to pick the container/folder.
7. **Endpoint Type**: select **Azure Function** and then choose your Function App and the specific Event Grid function (if already created) — otherwise configure later.

---

## 3. Create Azure Function project locally (Event Grid trigger)

1. In VS Code install Azure Functions and Azure Account extensions.
2. Create a new Function Project (Python):
   - Command Palette → `Azure Functions: Create New Project...` → choose folder → Python → venv → choose version → select Worker runtime `python`.
3. Add a **new function** → choose **Event Grid Trigger**.
4. The extension scaffolds:
   - `EventGridTrigger/__init__.py`
   - `EventGridTrigger/function.json`
   - `host.json` (project root)
5. Update `EventGridTrigger/__init__.py` to extract `data["url"]` and push a simple JSON to the storage queue using the queue output binding (or use SDK inside function).

Example `function.json` for event → queue:
```json
{
  "bindings": [
    {
      "type": "eventGridTrigger",
      "name": "event",
      "direction": "in"
    },
    {
      "type": "queue",
      "name": "outputQueueItem",
      "queueName": "ingestionqueue",
      "connection": "QueueConnection",
      "direction": "out"
    }
  ]
}
```

---

## 4. Run & Test Locally

1. Make sure Azure Functions Core Tools are installed (`func --version`).
2. Populate `local.settings.json` with local connection strings (do **not** commit):
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "<storage-conn-string>",
    "QueueConnection": "<storage-conn-string>",
    "FUNCTIONS_WORKER_RUNTIME": "python"
  }
}
```
3. Start functions locally:
```bash
func start
```
4. To simulate Event Grid you can push a queue message manually or run a local curl that calls the Event Grid function signature. Alternatively upload a blob to the storage container and allow the real Event Grid subscription to create the message in the queue.

---

## 5. Deploy Event Grid Function to Azure

1. In VS Code, sign into Azure.
2. Right-click the function project or use the Azure Functions extension → `Deploy to Function App`.
3. Choose an existing Function App or create a new one.
4. After deployment, go to the Function App → **Configuration** → add application settings:
   - `AzureWebJobsStorage` → storage connection string
   - `QueueConnection` → storage connection string (used by queue output binding)
   - `FUNCTIONS_WORKER_RUNTIME` → `python`

> **Important**: In production avoid storing secrets in app settings; use Key Vault and managed identity.

---

## 6. Create Storage Queue in the Storage Account

1. In Azure Portal → Storage account → **Queues** (under Data storage) → **+ Queue**.
2. Create queue named: `ingestionqueue`.
3. Azure will automatically create `ingestionqueue-poison` for poison messages; this is expected.

---

## 7. Connect Event Grid Subscription to Azure Function (Portal)

1. If you didn't select Azure Function when creating subscription, open the Event Subscription → **Edit** → **Endpoint type** → choose **Azure Function**.
2. Select the Function App and the Event Grid function in the list.
3. Save changes.
4. Now BlobCreated events will be delivered to your Function App which pushes to the storage queue.

---

## 8. Upload test files into the container folders

1. Go to Storage account → Containers → `raw` → open folder `atm` or `upi` or `customers`.
2. Click **Upload** and choose a sample file (e.g., `atm_transactions_10k.csv` into `raw/atm/`).
3. When the blob is uploaded Event Grid will generate an event that targets your EventGridTrigger function.
4. The function will validate the blob metadata and push a message to `ingestionqueue`.
5. You can monitor the queue: Storage account → Queues → `ingestionqueue` to see messages being added (as shown in your screenshot).

---

## 9. Monitoring & Troubleshooting

- **Function logs**: In Azure Portal → Function App → Functions → select function → Monitor / Logs (App Insights) to see execution logs.
- **Queue messages**: Portal → Storage account → Queues → `ingestionqueue`. Poison messages land in `ingestionqueue-poison`.
- **Event Grid**: Check Event Grid subscription metrics and delivery logs if events fail to deliver.
- **Permissions**: Ensure Function App has access to storage (connection strings or managed identity).

---

## 10. Result (screenshot)

Below is the screenshot showing messages in the `ingestionqueue` after uploading files to the `raw` container. This confirms the Event Grid → Function → Queue flow is working.

![ingestionqueue messages screenshot](/mnt/data/f8057a7e-d8e0-47ff-a4ee-8878ac3d3b49.png) 

---

## Notes & Best Practices

- Use **Managed Identity** for Function App to access Storage & Cosmos in production — avoid connection strings in app settings.
- For high-volume ingestion consider **Service Bus** (if ordering, sessions, or advanced features required).
- For python heavy workloads (pandas), consider running processing in Databricks or as a separate worker to avoid large function package sizes.
- Set up **Application Insights** for better observability.
- Configure **retry** logic and dead-letter handling for poison messages.

---

If you want, I can:
- Convert this README into a downloadable PDF.
- Add the exact commands/scripts you used to upload blobs and test.
- Generate Terraform to provision the storage account, event subscription, and queue automatically.
