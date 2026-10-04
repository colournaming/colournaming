import pytest

from colournaming.database import db
from colournaming.experimentcol.model import ColourTarget
from colournaming.experimentcolbg.model import BackgroundColour, ColourTargetColBG
from colournaming.mturk import controller as mturk_controller
from colournaming.mturkage import controller as mturkage_controller
from colournaming.namer.model import ColourCentroid, Language
from conftest import EN_CENTROIDS


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_import_centroids(app, runner):
    result = runner.invoke(args=["import-centroids", EN_CENTROIDS, "English", "en"])
    assert result.exit_code == 0, result.output
    assert Language.query.one().code == "en"
    assert ColourCentroid.query.count() == 30
    assert "en" in app.namers


def test_import_col_targets(runner, tmp_path):
    f = tmp_path / "targets.csv"
    f.write_text("id,red,green,blue\n1,2,3,4\n")
    result = runner.invoke(args=["import-col-targets", str(f)])
    assert result.exit_code == 0, result.output
    assert ColourTarget.query.one().blue == 4


def test_import_colbg_targets(runner, tmp_path, colbg_targets):
    f = tmp_path / "targets.csv"
    f.write_text("color_id,R,G,B\n9,2,3,4\n")
    result = runner.invoke(args=["import-colbg-targets", "--delete-existing", str(f)])
    assert result.exit_code == 0, result.output
    assert ColourTargetColBG.query.one().id == 9


def test_import_colbg_backgrounds(runner, tmp_path):
    f = tmp_path / "bgs.csv"
    f.write_text("bg_id,R,G,B,Label\n5,2,3,4,x\n")
    result = runner.invoke(args=["import-colbg-backgrounds", str(f)])
    assert result.exit_code == 0, result.output
    assert BackgroundColour.query.one().id == 5


@pytest.mark.parametrize("command", ["mturk-tasks", "mturk-age-tasks"])
def test_list_tasks_empty(runner, command):
    result = runner.invoke(args=[command])
    assert result.exit_code == 0, result.output
    assert result.output.splitlines() == ["completion_id,response_count"]


@pytest.mark.xfail(strict=True, reason="task models have no completion_id attribute")
@pytest.mark.parametrize(
    "command, controller",
    [("mturk-tasks", mturk_controller), ("mturk-age-tasks", mturkage_controller)],
)
def test_list_tasks(runner, command, controller):
    task = controller.create_mturk_task("pid", "study", "sess")
    participant_model = type(task).participant.property.mapper.class_
    db.session.add(participant_model(task=task))
    db.session.commit()
    result = runner.invoke(args=[command])
    assert result.exit_code == 0, result.output


def test_dropdb_and_initdb(runner):
    assert runner.invoke(args=["dropdb"]).exit_code == 0
    assert not db.inspect(db.engine).has_table("participants")
    assert runner.invoke(args=["initdb"]).exit_code == 0
    assert db.inspect(db.engine).has_table("participants")


def test_help(runner):
    result = runner.invoke(args=["help"])
    assert result.exit_code == 0
    assert "import-centroids" in result.output
