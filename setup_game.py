"""
SampleGame1 セットアップスクリプト
UE5エディタのOutputLogコンソールで実行: py "C:/Users/nabec/Documents/SampleGame1/setup_game.py"
"""
import unreal

CHAR_BP_PATH = "/Game/Project/Assets/Character/BP"
BLUEPRINTS_PATH = "/Game/Project/BluePrints"


def create_blueprint(name, parent_class_path, save_dir):
    """Blueprintアセットを作成して保存する"""
    full_path = f"{save_dir}/{name}"
    if unreal.EditorAssetLibrary.does_asset_exist(full_path):
        unreal.log(f"[skip] already exists: {name}")
        return unreal.load_asset(full_path)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.BlueprintFactory()

    if parent_class_path:
        parent_class = unreal.load_class(None, parent_class_path)
        if parent_class is None:
            unreal.log_warning(f"親クラスが見つかりません: {parent_class_path}")
            return None
        factory.set_editor_property("parent_class", parent_class)

    bp = asset_tools.create_asset(name, save_dir, unreal.Blueprint, factory)
    if bp:
        unreal.EditorAssetLibrary.save_asset(bp.get_path_name())
        unreal.log(f"[OK] 作成しました: {name}")
    else:
        unreal.log_error(f"[NG] 作成失敗: {name}")
    return bp


def add_box_component(bp, component_name="CollisionBox"):
    """BlueprintにBoxCollisionコンポーネントを追加する"""
    scs = bp.get_editor_property("simple_construction_script")
    if scs is None:
        return
    existing = [n.get_editor_property("internal_variable_name").to_string()
                for n in scs.get_all_nodes()]
    if component_name in existing:
        return
    node = scs.create_node_with_component_type(unreal.BoxComponent)
    if node:
        node.set_editor_property("internal_variable_name", unreal.Name(component_name))
        scs.add_node(node)
        unreal.log(f"  BoxComponent '{component_name}' を追加")


def add_static_mesh_component(bp, component_name="Mesh"):
    """BlueprintにStaticMeshComponentを追加する"""
    scs = bp.get_editor_property("simple_construction_script")
    if scs is None:
        return
    existing = [n.get_editor_property("internal_variable_name").to_string()
                for n in scs.get_all_nodes()]
    if component_name in existing:
        return
    node = scs.create_node_with_component_type(unreal.StaticMeshComponent)
    if node:
        node.set_editor_property("internal_variable_name", unreal.Name(component_name))
        scs.add_node(node)
        unreal.log(f"  StaticMeshComponent '{component_name}' を追加")


def add_niagara_component(bp, component_name="FireEffect"):
    """BlueprintにNiagaraParticleSystemComponentを追加する"""
    try:
        scs = bp.get_editor_property("simple_construction_script")
        if scs is None:
            return
        existing = [n.get_editor_property("internal_variable_name").to_string()
                    for n in scs.get_all_nodes()]
        if component_name in existing:
            return
        node = scs.create_node_with_component_type(unreal.NiagaraComponent)
        if node:
            node.set_editor_property("internal_variable_name", unreal.Name(component_name))
            scs.add_node(node)
            unreal.log(f"  NiagaraComponent '{component_name}' を追加")
    except Exception as e:
        unreal.log_warning(f"  Niagara追加をスキップ（Niagaraプラグイン確認要）: {e}")


def setup_bp_player():
    """BP_Player を BP_MyCharacter から作成"""
    bp = create_blueprint(
        "BP_Player",
        f"{CHAR_BP_PATH}/BP_MyCharacter.BP_MyCharacter_C",
        CHAR_BP_PATH,
    )
    if bp:
        add_static_mesh_component(bp, "Mesh")
        unreal.EditorAssetLibrary.save_asset(bp.get_path_name())
    return bp


def setup_bp_enemy():
    """BP_Enemy を BP_MyCharacter から作成"""
    bp = create_blueprint(
        "BP_Enemy",
        f"{CHAR_BP_PATH}/BP_MyCharacter.BP_MyCharacter_C",
        CHAR_BP_PATH,
    )
    if bp:
        unreal.EditorAssetLibrary.save_asset(bp.get_path_name())
    return bp


def setup_bp_goal():
    """BP_Goal を Actor から作成 (ゴール判定オブジェクト)"""
    bp = create_blueprint(
        "BP_Goal",
        "Blueprint'/Script/Engine.Actor'",  # Actor基底
        BLUEPRINTS_PATH,
    )
    if bp is None:
        # Actor クラスの別パス形式を試す
        factory = unreal.BlueprintFactory()
        factory.set_editor_property("parent_class", unreal.Actor)
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        full_path = f"{BLUEPRINTS_PATH}/BP_Goal"
        if not unreal.EditorAssetLibrary.does_asset_exist(full_path):
            bp = asset_tools.create_asset("BP_Goal", BLUEPRINTS_PATH, unreal.Blueprint, factory)
            if bp:
                unreal.EditorAssetLibrary.save_asset(bp.get_path_name())
                unreal.log("[OK] 作成しました: BP_Goal")
    if bp:
        add_box_component(bp, "GoalVolume")
        add_static_mesh_component(bp, "GoalMesh")
        unreal.EditorAssetLibrary.save_asset(bp.get_path_name())
    return bp


def setup_bp_dead_object():
    """BP_DeadObject に Niagara コンポーネントを追加（炎エフェクト用）"""
    bp = unreal.load_asset(f"{BLUEPRINTS_PATH}/BP_DeadObject")
    if bp is None:
        unreal.log_warning("BP_DeadObject が見つかりません")
        return
    add_niagara_component(bp, "FireEffect")
    unreal.EditorAssetLibrary.save_asset(bp.get_path_name())
    unreal.log("[OK] BP_DeadObject に FireEffect コンポーネントを追加")


def update_gamemode_default_pawn():
    """BP_MyGameMode のデフォルトポーンを BP_Player に変更"""
    gm_class = unreal.load_class(
        None, f"{BLUEPRINTS_PATH}/BP_MyGameMode.BP_MyGameMode_C"
    )
    if gm_class is None:
        unreal.log_warning("BP_MyGameMode が見つかりません")
        return
    player_class = unreal.load_class(
        None, f"{CHAR_BP_PATH}/BP_Player.BP_Player_C"
    )
    if player_class is None:
        unreal.log_warning("BP_Player が見つかりません（先に作成してください）")
        return
    cdo = gm_class.get_default_object()
    if cdo:
        cdo.set_editor_property("default_pawn_class", player_class)
        unreal.EditorAssetLibrary.save_asset(f"{BLUEPRINTS_PATH}/BP_MyGameMode")
        unreal.log("[OK] GameMode の DefaultPawn を BP_Player に設定")


def create_niagara_fire():
    """N_Fire Niagaraシステムを作成（Fountainテンプレートから）"""
    fire_path = "/Game/Project/Assets/Effects"
    full_path = f"{fire_path}/N_Fire"

    if unreal.EditorAssetLibrary.does_asset_exist(full_path):
        unreal.log("[skip] N_Fire already exists")
        return

    try:
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        factory = unreal.NiagaraSystemFactoryNew()
        ns = asset_tools.create_asset("N_Fire", fire_path, unreal.NiagaraSystem, factory)
        if ns:
            unreal.EditorAssetLibrary.save_asset(ns.get_path_name())
            unreal.log("[OK] N_Fire を作成しました（パラメータは手動調整が必要）")
        else:
            unreal.log_warning("N_Fire の自動作成に失敗。手動でNiagaraシステムを作成してください")
    except Exception as e:
        unreal.log_warning(f"Niagara自動生成スキップ: {e}")
        unreal.log("  → Content/Project/Assets/Effects/ フォルダに手動で N_Fire を作成してください")


def main():
    unreal.log("=" * 50)
    unreal.log("SampleGame1 セットアップ開始")
    unreal.log("=" * 50)

    with unreal.ScopedEditorTransaction("SampleGame1 Setup") as trans:
        setup_bp_player()
        setup_bp_enemy()
        setup_bp_goal()
        setup_bp_dead_object()
        update_gamemode_default_pawn()
        create_niagara_fire()

    unreal.log("=" * 50)
    unreal.log("セットアップ完了!")
    unreal.log("次の手順:")
    unreal.log("  1. BP_Player のイベントグラフに入力処理を追加")
    unreal.log("  2. BP_Goal のOnComponentBeginOverlapでゴール処理を実装")
    unreal.log("  3. N_Fire のパラメータをNiagaraエディタで調整")
    unreal.log("  4. SampleGame_1 レベルにオブジェクトを配置")
    unreal.log("=" * 50)


main()
