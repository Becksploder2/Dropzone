from pathlib import Path
p=Path("DropZone_Godot4/scripts/main.gd")
s=p.read_text()
assert 'func show_menu() -> void:' in s
assert 'func render_bridge() -> void:' in s
assert 'func create_ui() -> void:' in s
# The former fullscreen ColorRect intercepted GUI input in some layouts.
s=s.replace(' overlay = ColorRect.new()\n', ' overlay = ColorRect.new()\n overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE\n',1)
s=s.replace(' ui = Control.new()\n', ' ui = Control.new()\n ui.mouse_filter = Control.MOUSE_FILTER_PASS\n',1)
s=s.replace(' margin = MarginContainer.new()\n',' margin = MarginContainer.new()\n margin.mouse_filter = Control.MOUSE_FILTER_PASS\n',1)
# Explicit zero-configuration play flow, retaining customization as optional.
s=s.replace('button("PLAY — Solo / AI / Local Team",func(): start_game())','button("PLAY NOW — default contestant + 2 AI teammates",start_game)\n button("PLAY — Solo / AI / Local Team",start_game)',1)
# Panels can be reached via GUI even on unusual screen sizes or if the viewport masks a ray cast.
needle=' if ai[current_player]: button("AUTO PLAY AI TURN",ai_turn)\n button("BACK TO MAIN MENU",show_menu)'
assert needle in s
s=s.replace(needle,''' if not ai[current_player]:
  text_line("Choose an answer below OR click its 3D panel. Your contestant walks to lock it in.")
  for choice in range(groups[tier_index].size()):
   var answer_index=choice
   button("STEP ON: %s" % str(groups[tier_index][choice]["text"]),func(): select_answer(answer_index))
 else:
  button("AUTO PLAY AI CONTESTANT",ai_turn)
 button("BACK TO MAIN MENU",show_menu)''',1)
# Show avatar and stage with an unobstructed wide game camera instead of the preview camera.
needle=' characters[current_player].position=Vector3(0,0,-7.0)\n load_question()'
if needle in s:
 s=s.replace(needle,''' characters[current_player].position=Vector3(0,0,-7.0)
 camera.position=Vector3(14,12,19)
 camera.look_at(Vector3(0,0,0),Vector3.UP)
 ui.visible=true
 load_question()''',1)
# Make main menu robust on re-entering after previous preview.
needle='func show_menu() -> void:\n game_state = "menu"'
assert needle in s
s=s.replace(needle,'''func show_menu() -> void:
 game_state = "menu"
 ui.visible = true''',1)
# In prototype panel selection is still driven by clicks; avoid the entire screen trapping those clicks.
# The on-screen choice buttons provide a guaranteed keyboard/mouse navigable control.
p.write_text(s)
print("Installed menu/quick-play/bridge control hotfix")
