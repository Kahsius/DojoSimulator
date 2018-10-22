# DojoSimulator

## What it is ?

Dojo Simulator is a python script running a set of matches of the prototype game "Dojo, duel of masters". The results are then used to balance the game depending on the results of each character (Prodigy).

## Usage

Simply clone the project and run the following command :
```shell
python main.js -n N_TEST -v
```
with -n N_TEST the number of games you want the simulator to play (default 10 000) and -v a flag to specify if the simulator should display all the played games. It's preferable to keep N_TEST low when this flag is up.

If you want to modify a character, you have to write in data/prodigies.json. You can create, modify or remove any character you want. You can even modify the effects of the Voies in data/voies.json.

## GUI

You can also launch the simulator in a simplistic GUI by running :
```shell
python gui.py
```

## Results

After the N_TEST games, the script displays various statistical results on the prodigies and the voies.
