# 1. Configure .env file in source dir similar to this below:
```.env
# The URL where online data must be pulled from
URL="https://some-website.com/data-list" 
# The Playwright locator id that is on the URL page 
LOCATOR_ID="a[id=link-id]"

TEST_DATA="predict_data.txt"

# Keywords to look out for to alter Tensorflow model's prediction values (see util/check_prediction.py)
KEYWORDS="Construction, Astronomy, Sillicone"

TRAINING_DATA_SET="maven_training_data.json"

ENTRY_TEXT_TITLE="some text title"

ENTRY_LABEL_TITLE="expected_positive_or_negative_label"

POSITIVE_LABEL="1"

NEGATIVE_LABEL="0"
```
# 2. Add input_training_data.json in this format to train Tensorflow model:
```
[
  {
      "ENTRY_TEXT_TITLE": "some text title",
      "ENTRY_LABEL_TITLE": "expected_positive_or_negative_label" 
  },
  ...
]
```

Once training data is complete, set file name to the .env variable above within `training_data` dir.
# 3. Building the Containerized Application
### 1. Make sure to install podman globally
https://podman.io/docs/installation

### 2. Start Podman or Docker Machine
`podman machine start`

### 3. Build Podman or Docker container from Containerfile with img title of maven
`podman build . -t maven`

### 4. Wait some time for Container to build
This process usually takes up to 8 minutes depending on user's machine

### 5. Run the Container
`podman run -it maven`

### 6. Within another terminal, exec into podman container
`podman exec -it <container_id> sh`

# 4. Using the Application
The following steps should be performed in this order:
### 1. Using frontend
`cd frontend` \
`yarn playwright install` \
`yarn start`

This then grabs and fills the text file (TEST_DATA env) with lines of data based on what was pulled from (LOCATOR_ID env)
### 2. Building and training Tensorflow model
Make sure user is in top-level dir \
`python model.py` \
This uses the training data (TRAINING_DATA_SET env) to train the model. Having this env variable is integral for this step to work
### 3. Predicting from the TEST_DATA env text file
`python predict.py` \
This then logs true or false positive or negatives according to its acquainted log json file