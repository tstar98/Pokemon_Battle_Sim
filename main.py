
# MUST import from top-level or it gets a different instance from GUI scripts
from Pokemon_Battle_Sim.Model import Model
from Pokemon_Battle_Sim import use_gui
from Pokemon_Battle_Sim import demo

if __name__ == '__main__':
    if use_gui:
        # Initialize GUI
        from gui.root import Root, menus
        root = Root()
        # root.open_menu(menus.BATTLE)
        root.open_menu(menus.MAIN_MENU)
        root.mainloop()
    else:
        # Run in console
        from Pokemon_Battle_Sim import BattleBackend
        
        #
        demo.demo1(make_player=True)
        #
        # input("Press enter to continue.")
        # demo.demo1(make_player=True)
        #
        # input("Press enter to continue.")
        # demo.demo2(make_player=True)
        
        battle = BattleBackend.Battle()
        while Model.player.has_pokemon() and Model.opponent.has_pokemon():
            battle.battle_round()
