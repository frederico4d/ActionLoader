# BlenderScripts
Action Loader
ActionLoader.py

Action Loader is an addon for quickly displaying and loading actions into a model. It was done particularly to manage multiple actions / animations on the same character, for game animations.

preview: https://www.youtube.com/watch?v=aQrfsufhyWw

## How to use?

I have automated most things, so you just have to select an object, usually an armature, and select the action from the list.

- It will automatically save the current frame range (preview frame range) on the current action, apply the newly selected action, set the frame range on the scene to the selected action range, and zoom on all time viewers (Timeline Dopesheet Editor and Graph Editor). You can even do that while playing the animations in loop for a really quick preview of all your work.

- It also ads fake users to the actions automatically so you don't have to think about it nor worry about loosing actions

- There is a filter in the list, so that if you have hundreads of animations, just carefully name them, and use that filter to display only a set of animations, for example, fighting animations can have a tag in the name, and you filter for it etc...

- It also displays some information about the actions, that can be helpfull, currently the name, number of frames (from the frame range) and duration in seconds.

### Bugs
- When objects don't have actions that can give some errors, but it is ok to continue to use, I fixed some of those but probably not all.

- In some situations when the action doesn't have frame range defined yet, it can give a bug but you can continue to use it, it will automatically set it on next click.

- It sometimes crashes blender when deleting actions, can't fix this yet.

- Any tips, ideas or help is welcome.

