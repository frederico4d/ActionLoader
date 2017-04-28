# BlenderScripts
Action Loader
ActionLoader.py

Action Loader is an addon for quickly displaying and loading actions into a model. It was done particularly to manage multiple actions / animations on the same character, for game animations.

preview: https://www.youtube.com/watch?v=aQrfsufhyWw

## How to use?

I have automated most things, so you just have to select an object, usually an armature, and select the actions from the list.
And you get:

- It will automatically save the current frame range on the current action, apply the newly selected action, set the frame range on the scene from the selected action, and zoom in on all time viewers (Timeline Dopesheet Editor and Graph Editor). 

- You can even do that while playing the animations in loop for a really quick preview of all your work.

- It also ads fake users to the actions automatically so you don't have to think about it nor worry about loosing actions

- There is a filter in the list, so that if you have hundreads of animations, just carefully name them, and use that filter to display only a set of animations, for example, fighting animations can have a tag in the name, and you filter for it etc...

- It also displays some information about the actions, that can be helpfull, currently the name, number of frames (from the frame range) and duration in seconds. 

- Other info: shows the total number of animations in the file and number of listed (filtered) animations.

### To do

- Be able to add an action to objects that don't have any yet.

Any comments, ideas etc... are welcome, please issue them!
