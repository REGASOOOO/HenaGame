def test_game_import():
    import src.game as game
    assert hasattr(game, "run_game")
