from pathlib import Path
p = Path("DropZone_Godot4/scripts/main.gd")
s = p.read_text()
if "func show_stage_preview()" in s:
    raise SystemExit("Stage preview already installed")
s = s.replace("var awaiting_drop := false", "var awaiting_drop := false\nvar stage_preview := false")
s = s.replace(" camera = Camera3D.new()", """ # Audience terraces and studio accents.
 for side in [-1,1]:
  for row_idx in range(4):
   var x_pos = float(side) * (10.3 + float(row_idx) * 0.7)
   box_mesh(stage,Vector3(x_pos,-0.15+row_idx*0.45,0),Vector3(1.25,0.65,15),Color("18264a"))
   for seat_idx in range(9):
    var z_pos = float(seat_idx)*1.6-6.4
    box_mesh(stage,Vector3(x_pos,0.45+row_idx*0.45,z_pos),Vector3(0.5,0.65,0.5),Color("375e91") if (seat_idx+row_idx)%2==0 else Color("2e497a"))
 for x_pos in [-8.3,8.3]:
  box_mesh(stage,Vector3(x_pos,0.02,0),Vector3(0.12,0.13,14),Color("45d8ff"))
 for y_pos in [0.6,3.9]:
  box_mesh(stage,Vector3(0,y_pos,-8),Vector3(18,0.12,0.18),Color("36bfff"))
 for x_pos in [-9.0,9.0]:
  box_mesh(stage,Vector3(x_pos,2.25,-8),Vector3(0.14,3.4,0.18),Color("36bfff"))
 for light_pos in [Vector3(-7,6,3),Vector3(7,6,3),Vector3(0,8,-4)]:
  var spot = OmniLight3D.new()
  spot.position = light_pos
  spot.light_color = Color("56bfff")
  spot.light_energy = 1.9
  spot.omni_range = 14.0
  stage.add_child(spot)
 camera = Camera3D.new()""")
s = s.replace(' button("PLAY — Solo / AI / Local Team",func(): start_game())',' button("PLAY — Solo / AI / Local Team",func(): start_game())\n button("VIEW 3D SET (ESC to return)",show_stage_preview)')
s = s.replace("func show_contestants() -> void:", """func show_stage_preview() -> void:
 stage_preview = true
 game_state = "preview"
 ui.visible = false
 camera.position = Vector3(19,14,22)
 camera.look_at(Vector3(0,1,-1),Vector3.UP)

func _unhandled_key_input(event: InputEvent) -> void:
 if stage_preview and event.is_action_pressed("ui_cancel"):
  stage_preview = false
  ui.visible = true
  camera.position = Vector3(15,15,19)
  camera.look_at(Vector3(0,0,0),Vector3.UP)
  show_menu()
  get_viewport().set_input_as_handled()

func show_contestants() -> void:""")
s = s.replace(' overlay.visible = true\n clear_controls()\n heading.text = "DROP ZONE"', ' overlay.visible = true\n overlay.color = Color(0.025,0.045,0.11,0.76)\n clear_controls()\n heading.text = "DROP ZONE"')
s = s.replace("func render_bridge() -> void:\n overlay.visible = true", "func render_bridge() -> void:\n overlay.visible = true\n overlay.color = Color(0.025,0.045,0.11,0.12)")
p.write_text(s)
