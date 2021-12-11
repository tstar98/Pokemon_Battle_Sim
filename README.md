# Pokemon Battle Simulator
Thomas Starnes and Brian Glassman

## OOAD
For this project we used Python 3. 

The code revolves around an abstract class Move that is inheritted by all Move subclasses. We use move factory to generate the correct class of a given move.

Classes like StatusEffectAttack and StatAlteringAttack are concrete decorators. They call super.use_move() and then add an additional function such as applying a status effect or lowering the opponent's stats.

LevelBasedAttack uses strategy to determine the damage done. Most LevelBasedAttacks apply damage equal to the user's level, but Psybeam adds a random modifier of 1 to 1.5 * to that damage.

MVC or PubSub

## Insructions
### Main Menu and Team Building
To play Pokemon Battle Simulator, simply run main.py. The game will launch and display the main menu. There you can select to build your own team or play one of our 3 demos. The demos have prebuilt teams of 3 Pokemon with 4 preselected moves each that the user can use and will go up against a bot. You can also build your own team. To do this, select a Pokemon you wish to use. Once you have clicked on the Pokemon's name, you will be shown the moves it can learn. Click on the move you wish to use and click "Add Move." Once you have at least one move and no more than four moves, select "Add to team" to add that Pokemon with those selected moves to your team. Once you have 3 Pokemon on your team, click "Battle!" in the top left corner to begin your battle.

### Battle
Once the battle has begun, you will be shown the the moves of your Pokemon. Select the move you wish to use that turn. The battle will display the message of whatever happens that turn. Once you have read the message, click on the text box and you will be shown the move menu once again.
