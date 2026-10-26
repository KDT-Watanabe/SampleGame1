"""
SampleGame_1 レベルにオブジェクトを配置するスクリプト
setup_game.py 実行後に使用。
UE5エディタのOutputLogコンソールで実行:
  py "C:/Users/nabec/Documents/SampleGame1/setup_level.py"
"""
import unreal

LEVEL_PATH = "/Game/Project/Levels/SampleGame_1/SampleGame_1"
BP_PATH = "/Game/Project/BluePrints"
CHAR_BP_PATH = "/Game/Project/Assets/Character/BP"


def open_sample_level():
    """SampleGame_1 レベルを開く"""
    unreal.EditorLevelLibrary.load_level(LEVEL_PATH)
    unreal.log(f"[OK] レベルを開きました: {LEVEL_PATH}")


def spawn_actor(bp_path, location, rotation=(0, 0, 0), label=None):
    """指定BPをレベルに配置する"""
    bp_class = unreal.load_class(None, f"{bp_path}_C")
    if bp_class is None:
        # アセットとして試す
        asset = unreal.load_asset(bp_path)
        if asset and hasattr(asset, 'generated_class'):
            bp_class = asset.generated_class()
    if bp_class is None:
        unreal.log_warning(f"クラスが見つかりません: {bp_path}")
        return None

    loc = unreal.Vector(*location)
    rot = unreal.Rotator(*rotation)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(bp_class, loc, rot)
    if actor and label:
        actor.set_actor_label(label)
    return actor


def setup_level():
    """レベルにゲームオブジェクトを配置"""
    open_sample_level()

    unreal.log("オブジェクトを配置中...")

    # フロア（既存のメッシュを使用）
    # BP_Key を配置（2個）
    spawn_actor(f"{BP_PATH}/BP_Key", (200, 0, 100), label="Key_1")
    spawn_actor(f"{BP_PATH}/BP_Key", (-200, 300, 100), label="Key_2")

    # BP_Door を配置
    spawn_actor(f"{BP_PATH}/BP_Door", (500, 0, 0), (0, 0, 90), label="Door_1")

    # BP_SwitchButton を配置
    spawn_actor(f"{BP_PATH}/BP_SwitchButton", (0, 400, 50), label="SwitchButton_1")

    # BP_Lever を配置
    spawn_actor(f"{BP_PATH}/BP_Lever", (-300, 0, 50), label="Lever_1")

    # BP_DeadObject (炎ダメージ) を配置
    spawn_actor(f"{BP_PATH}/BP_DeadObject", (100, -300, 50), label="DamageObject_1")
    spawn_actor(f"{BP_PATH}/BP_DeadObject", (-100, -300, 50), label="DamageObject_2")

    # BP_Goal を配置（ゴール地点）
    spawn_actor(f"{BP_PATH}/BP_Goal", (800, 0, 100), label="Goal")

    # プレイヤースタート位置は PlayerStart を使用
    unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PlayerStart,
        unreal.Vector(0, 0, 100),
        unreal.Rotator(0, 0, 0),
    )

    # レベルを保存
    unreal.EditorLevelLibrary.save_current_level()
    unreal.log("[OK] レベルの配置が完了しました")
    unreal.log("※ 位置は手動で調整してください")


setup_level()
