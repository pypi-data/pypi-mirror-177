#!/usr/bin/env python

import os
from urllib.parse import urlparse

import requests


class Client:

    output_style = "json"

    def __init__(self, api_token=None, host=None, proto=None, ssl_cert_verify=None):
        self.host = host if host else os.environ.get("ANOMALO_INSTANCE_HOST")
        self.api_token = (
            api_token if api_token else os.environ.get("ANOMALO_API_SECRET_TOKEN")
        )

        if not self.host:
            raise RuntimeError(
                "Please specify Anomalo instance host via ANOMALO_INSTANCE_HOST env var"
            )
        if not self.api_token:
            raise RuntimeError(
                "Please specify Anomalo api token via ANOMALO_API_SECRET_TOKEN env var"
            )

        parsed_host_url = urlparse(self.host)
        host_scheme = parsed_host_url.scheme
        if host_scheme:
            self.proto = host_scheme
            self.host = parsed_host_url.netloc
        else:
            self.proto = proto if proto else "https"

        self.request_headers = {"X-Anomalo-Token": self.api_token}

        self.verify = ssl_cert_verify

    def _api_call(self, endpoint, method="GET", **kwargs):

        endpoint_url = "{proto}://{host}/api/public/v1/{endpoint}".format(
            proto=self.proto, host=self.host, endpoint=endpoint
        )

        if method in ["PUT", "POST"]:
            request_args = dict(json=kwargs)
        else:
            request_args = dict(params=kwargs)
        r = requests.request(
            method,
            endpoint_url,
            headers=self.request_headers,
            verify=self.verify,
            allow_redirects=False,
            **request_args,
        )

        if not r.ok:
            raise RuntimeError(r.text)
        return r.json() if self.output_style == "json" else r.text

    def ping(self):
        return self._api_call("ping")

    def get_active_organization_id(self):
        return self._api_call("organization").get("id")

    def set_active_organization_id(self, organization_id):
        return self._api_call("organization", method="PUT", id=organization_id).get(
            "id"
        )

    def get_all_organizations(self):
        return self._api_call("organizations")

    def list_warehouses(self):
        return self._api_call("list_warehouses")

    def refresh_warehouse(self, warehouse_id):
        return self._api_call(f"warehouse/{warehouse_id}/refresh", method="PUT")

    def refresh_warehouse_tables(self, warehouse_id, table_full_names):
        if not table_full_names:
            raise RuntimeError("Must specify a list of full table names to sync")
        return self._api_call(
            f"warehouse/{warehouse_id}/refresh",
            method="PUT",
            table_full_names=table_full_names,
        )

    def refresh_warehouse_new_tables(self, warehouse_id):
        return self._api_call(f"warehouse/{warehouse_id}/refresh/new", method="PUT")

    def list_notification_channels(self):
        return self._api_call("list_notification_channels")

    def configured_tables(self, check_cadence_type=None, warehouse_id=None):
        return self._api_call(
            "configured_tables",
            check_cadence_type=check_cadence_type,
            warehouse_id=warehouse_id,
        )

    def get_table_information(self, warehouse_id=None, table_id=None, table_name=None):
        if (not table_id or not warehouse_id) and not table_name:
            raise RuntimeError(
                "Must specify either warehouse_id & table_id or table_name for get_table_information"
            )
        else:
            return self._api_call(
                "get_table_information",
                warehouse_id=warehouse_id,
                table_id=table_id,
                table_name=table_name,
            )

    def get_check_intervals(self, table_id=None, start=None, end=None):
        if not table_id:
            raise RuntimeError("Must specify a table_id for get_check_intervals")
        else:
            results = []
            page = 0
            paged_results = None
            while paged_results is None or len(paged_results) > 0:
                paged_results = self._api_call(
                    "get_check_intervals",
                    table_id=table_id,
                    start=start,
                    end=end,
                    page=page,
                )["intervals"]
                results.extend(paged_results)
                page = page + 1
            return results

    def get_checks_for_table(self, table_id):
        return self._api_call("get_checks_for_table", table_id=table_id)

    def run_checks(self, table_id, interval_id=None, check_ids=None):
        if check_ids:
            if not isinstance(check_ids, list) and not isinstance(check_ids, tuple):
                check_ids = [check_ids]
            check_ids = list(check_ids)  # Convert from Tuple
            return self._api_call(
                "run_checks",
                method="POST",
                table_id=table_id,
                interval_id=interval_id,
                check_ids=check_ids,
            )
        else:
            return self._api_call(
                "run_checks",
                method="POST",
                table_id=table_id,
                interval_id=interval_id,
            )

    def get_run_result(self, job_id):
        return self._api_call("get_run_result", run_checks_job_id=job_id)

    def get_run_result_triage_history(self, job_id):
        return self._api_call("get_run_result_triage_history", run_checks_job_id=job_id)

    def create_check(self, table_id, check_type, **params):
        return self._api_call(
            "create_check",
            table_id=table_id,
            check_type=check_type,
            method="POST",
            params=params,
        )

    def delete_check(self, table_id, check_id):
        return self._api_call(
            "delete_check",
            table_id=table_id,
            check_id=check_id,
            method="POST",
        )

    def clone_check(self, table_id, check_id, new_table_id):
        return self._api_call(
            "clone_check",
            table_id=table_id,
            check_id=check_id,
            new_table_id=new_table_id,
            method="POST",
        )

    def configure_table(
        self,
        table_id,
        *,
        check_cadence_type=None,
        definition=None,
        time_column_type=None,
        notify_after=None,
        time_columns=None,
        fresh_after=None,
        interval_skip_expr=None,
        notification_channel_id=None,
        slack_users=None,
        check_cadence_run_at_duration=None,
    ):
        time_columns = [] if time_columns is None else time_columns
        slack_users = {} if slack_users is None else slack_users

        return self._api_call(
            "configure_table",
            table_id=table_id,
            method="POST",
            check_cadence_type=check_cadence_type,
            definition=definition,
            time_column_type=time_column_type,
            notify_after=notify_after,
            notification_channel_id=notification_channel_id,
            time_columns=time_columns,
            fresh_after=fresh_after,
            interval_skip_expr=interval_skip_expr,
            slack_users=slack_users,
            check_cadence_run_at_duration=check_cadence_run_at_duration,
        )


def main():
    import fire

    Client.output_style = "text"

    fire.Fire(Client)


if __name__ == "__main__":
    main()
