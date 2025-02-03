import pytest
import csv
import uuid
import json
from pathlib import Path
from API_Automation.E2E_Framework.A_centrlized_file import api_ulits
from API_Automation.E2E_Framework.base_config import Env, clients

baseURLs = get_URL(Env, clients)

campaigns_endpoint = "campaigns"

TEMPLATE_CSV_PATH = Path(
    r"/API_Auotmation/edda29879786e996d997e8963c7c2435/E2E_Framework/Test_runner_folder/Test_Data/Template_ID/template_ids.csv")
RECIPIENT_CSV_PATH = Path(
    r"/API_Auotmation/edda29879786e996d997e8963c7c2435/E2E_Framework/Test_runner_folder/Test_Data/Recipients_ID/recipient_list_ids.csv")

if not TEMPLATE_CSV_PATH.exists() or not RECIPIENT_CSV_PATH.exists():
    pytest.fail("Error: CSV files are missing")


def read_csv(file_path, column_name):
    data_list = []
    try:
        with open(file_path, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames

            if not headers or column_name not in headers:
                pytest.fail(f"Error: Column '{column_name}' not found in {file_path}. Available columns: {headers}")

            for row in reader:
                data_list.append(row[column_name])

    except Exception as e:
        pytest.fail(f"Error reading CSV file {file_path}: {e}")

    return data_list


template_ids = read_csv(TEMPLATE_CSV_PATH, "Template ID")
recipient_list_ids = read_csv(RECIPIENT_CSV_PATH, "Recipient List ID")

if not template_ids or not recipient_list_ids:
    pytest.fail("Error: Missing template IDs or recipient list IDs")


def generate_campaign_name():
    return f"Campaign_{uuid.uuid4().hex[:8]}"


class TestCampaigns:
    created_campaigns = []

    @pytest.mark.order(5)
    def test_create_campaigns(self):
        for client in clients:
            baseURL = baseURLs.get(client)
            if not baseURL:
                pytest.fail(f"Base URL not found for client '{client}'")

            if client == "campaigns":
                url = f"{baseURL}/{campaigns_endpoint}"

                try:
                    for i in range(min(len(template_ids), len(recipient_list_ids))):
                        campaign_name = generate_campaign_name()
                        payload = {
                            "campaignName": campaign_name,
                            "emailTemplateId": template_ids[i],
                            "recipientListId": recipient_list_ids[i],
                            "scheduledTime": 0
                        }

                        response = api_ulits.postDATA(url, payload)
                        assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

                        response_json = response.json()
                        assert response_json.get("meta", {}).get("status") == "SUCCESS"

                        campaign_id = response_json["data"]["id"]
                        self.created_campaigns.append((campaign_id, campaign_name))

                except json.JSONDecodeError:
                    pytest.fail(f"Response is not valid JSON: {response.text}")
                except Exception as e:
                    pytest.fail(f"Error in campaign creation: {e}")

    @pytest.mark.order(6)
    def test_update_campaign_name(self):
        if not self.created_campaigns:
            pytest.fail("No campaign data available. Run `test_create_campaigns` first.")

        updated_campaigns = []
        for client in clients:
            base_path = baseURLs.get(client)
            if not base_path:
                pytest.fail(f"Base path not found for client '{client}'")

            if client == "campaigns":
                try:
                    for campaign_id, old_campaign_name in self.created_campaigns:
                        patch_url = f"{base_path.rstrip('/')}/{campaigns_endpoint}/{campaign_id}/name"
                        new_campaign_name = generate_campaign_name()
                        update_payload = {"campaignName": new_campaign_name}

                        patch_response = api_ulits.patchDATA(patch_url, update_payload)
                        assert patch_response.status_code == 200, f"Expected status code 200, but got {patch_response.status_code}"

                        response_json = patch_response.json()
                        assert response_json.get("meta", {}).get("status") == "SUCCESS"

                        updated_name = response_json["data"]["campaignName"]
                        assert updated_name == new_campaign_name, f"Campaign name did not update. Expected: {new_campaign_name}, Got: {updated_name}"

                        updated_campaigns.append((campaign_id, updated_name))

                except json.JSONDecodeError:
                    pytest.fail(f"Response is not valid JSON: {patch_response.text}")
                except Exception as e:
                    pytest.fail(f"Error in campaign update: {e}")

        return updated_campaigns

    @pytest.mark.order(7)
    def test_get_campaign_and_validate_update(self):
        updated_campaigns = self.test_update_campaign_name()
        if not updated_campaigns:
            pytest.fail("No updated campaign data available. Run `test_update_campaign_name` first.")

        for client in clients:
            base_path = baseURLs.get(client)
            if not base_path:
                pytest.fail(f"Base path not found for client '{client}'")

            if client == "campaigns":
                try:
                    for campaign_id, expected_name in updated_campaigns:
                        get_url = f"{base_path.rstrip('/')}/{campaigns_endpoint}/{campaign_id}"

                        get_response = api_ulits.getDATA(get_url)
                        assert get_response.status_code == 200, f"Expected status code 200, but got {get_response.status_code}"

                        response_json = get_response.json()
                        assert "data" in response_json

                        retrieved_name = response_json["data"]["campaignName"]
                        assert retrieved_name == expected_name, f"Campaign name mismatch. Expected: {expected_name}, Got: {retrieved_name}"

                except json.JSONDecodeError:
                    pytest.fail(f"Response is not valid JSON: {get_response.text}")
                except Exception as e:
                    pytest.fail(f"Error in campaign validation: {e}")
