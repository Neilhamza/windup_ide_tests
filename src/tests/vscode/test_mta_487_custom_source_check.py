import pytest

APP_NAME = "custom source check"


@pytest.mark.parametrize("app_name", [APP_NAME])
@pytest.mark.parametrize(
    "analysis_data",
    [
        {
            APP_NAME: {"options": {"target": ["eap 7"], "source": ["custom_source", "custom_source_1"]}},
        },
    ],
)
@pytest.mark.parametrize("ide", ["vscode"])
@pytest.mark.vscode
def test_mta_487_custom_source_check(setup_vscode, configurations, app_name, analysis_data, ide):
    # Automates Polarion MTA-487

    vscode = setup_vscode

    configuration_object, _, _ = configurations

    sources_list = configuration_object.configurations[0].options.source

    vscode.set_focus()
    vscode.run_simple_analysis(app_name)
    vscode.cancel_analysis()

    command_map = vscode.fetch_executed_cli_command_map()
    command_source = command_map["source"]

    assert set(command_source) == set(sources_list), f"Error: the following sources were not picked by the IDE: {','.join([src for src in sources_list if src not in command_source])}"
