from pathlib import Path
import re
p=Path("DropZone_Godot4/scripts/main.gd")
s=p.read_text()
def swap(name,src):
 global s
 pat=r"^func "+name+r"\([\s\S]*?(?=^func |\Z)"
 s,count=re.subn(pat,lambda m:src+"\n\n",s,count=1,flags=re.M|re.S)
 if count!=1:raise RuntimeError("Missing function "+name)
s=s.replace("var awaiting_drop := false","""var awaiting_drop := false
var bridge_panels: Array=[]
var bridge_groups: Array=[]
var row_index := 0
const ROW_COUNTS=[3,3,2,1]""",1)
s=s.replace("  tiles.append(tile)","  tiles.append(tile)\n  tile.visible=false",1)
s=s.replace(" enhance_full_studio()\n create_ui()"," enhance_full_studio()\n install_branching_bridge()\n create_ui()",1)
s=s.replace("Each contestant must choose 3 safe panels to cross. A wrong choice drops them. The studio audience knows the drop zones, but cannot help.","Each contestant crosses 3 / 3 / 2 / 1 answer panels. Click the actual bridge panel to step on your answer. Only wrong choices drop. The audience knows but must stay silent.")
s=s.replace("AI contestants select automatically; human contestants click an answer panel. A question contains 8 choices and at least 3 safe answers.","Human players click a 3D panel to lock their answer. Each row has one correct choice; AI uses AUTO PLAY.")
swap("begin_next_contestant",'''func begin_next_contestant() -> void:
 if crossing>=3:
  end_round()
  return
 current_player=crossing
 if not alive[current_player]:
  crossing+=1
  begin_next_contestant()
  return
 row_index=0
 step_count=0
 awaiting_drop=false
 characters[current_player].position=Vector3(0,0,-7)
 characters[current_player].visible=true
 load_question()''')
swap("load_question",'''func load_question() -> void:
 var available=[]
 for i in range(question_bank.size()):
  if not used_question_ids.has(i) and question_bank[i].get("correct",[]).count(true)>=3 and question_bank[i].get("correct",[]).count(false)>=2:
   available.append(i)
 if available.is_empty():
  used_question_ids=[]
  for i in range(question_bank.size()):
   if question_bank[i].get("correct",[]).count(true)>=3 and question_bank[i].get("correct",[]).count(false)>=2:
    available.append(i)
 if available.is_empty():
  show_reveal("Please add questions with both correct and incorrect options.",show_menu)
  return
 var id=int(available.pick_random())
 used_question_ids.append(id)
 current_question=question_bank[id]
 var truths=[]
 var lies=[]
 for i in range(current_question["answers"].size()):
  if bool(current_question["correct"][i]): truths.append(i)
  else: lies.append(i)
 truths.shuffle()
 lies.shuffle()
 bridge_groups=[]
 var right_i=0
 var wrong_i=0
 for row_count in ROW_COUNTS:
  var group=[{"label":str(current_question["answers"][truths[right_i%truths.size()]]),"correct":true}]
  right_i+=1
  for j in range(int(row_count)-1):
   group.append({"label":str(current_question["answers"][lies[wrong_i%lies.size()]]),"correct":false})
   wrong_i+=1
  group.shuffle()
  bridge_groups.append(group)
 refresh_bridge_panels()
 render_bridge()''')
swap("render_bridge",'''func render_bridge() -> void:
 overlay.visible=true
 overlay.color=Color(0.015,0.025,0.055,0.12)
 clear_controls()
 heading.text="ROUND %d  |  CROSSING %d/3" % [round_num,crossing+1]
 info.text="%s | ROW %d/4 | BANK $%d" % [contestants[current_player],row_index+1,bank]
 text_line("%s — %s" % [current_question.get("mode","TRUTH"),current_question.get("prompt","")])
 text_line("CLICK a physical answer panel on the bridge to step onto it.")
 for i in range(bridge_groups[row_index].size()):
  text_line("%d. %s" % [i+1,bridge_groups[row_index][i]["label"]])
 if ai[current_player]: button("AUTO PLAY AI TURN",ai_turn)
 button("BACK TO MAIN MENU",show_menu)''')
swap("ai_turn",'''func ai_turn() -> void:
 if game_state!="crossing" or not ai[current_player] or awaiting_drop: return
 var good=[]
 var bad=[]
 for i in range(bridge_groups[row_index].size()):
  if bridge_groups[row_index][i]["correct"]:good.append(i)
  else:bad.append(i)
 var selected=good if rng.randf()<difficulty or bad.is_empty() else bad
 select_answer(int(selected.pick_random()))''')
swap("select_answer",'''func select_answer(idx: int) -> void:
 if game_state!="crossing" or awaiting_drop:return
 if idx<0 or idx>=bridge_groups[row_index].size():return
 awaiting_drop=true
 selected_answer=idx
 var item:Dictionary=bridge_panels[row_index][idx]
 var target:Vector3=item["position"]
 var model:MeshInstance3D=item["mesh"]
 model.material_override=material(Color("f0bf63"))
 var walk=create_tween()
 walk.tween_property(characters[current_player],"position",Vector3(target.x,0,target.z),0.65)
 clear_controls()
 heading.text="IS THAT A DROP ZONE?"
 info.text="%s stepped on %s" % [contestants[current_player],bridge_groups[row_index][idx]["label"]]
 text_line("Karli-Rae: 'Is... that... a DROP ZONE?'")
 button("REVEAL PANEL",reveal_panel)''')
swap("reveal_panel",'''func reveal_panel() -> void:
 if not awaiting_drop:return
 awaiting_drop=false
 var safe=bool(bridge_groups[row_index][selected_answer]["correct"])
 var item:Dictionary=bridge_panels[row_index][selected_answer]
 var panel:MeshInstance3D=item["mesh"]
 panel.material_override=material(Color("11dd85") if safe else Color("e32a4d"))
 if safe:
  row_index+=1
  step_count=row_index
  if row_index>=ROW_COUNTS.size():
   successful+=1
   crossing+=1
   show_reveal("SAFE! %s crossed the bridge." % contestants[current_player],func():begin_next_contestant())
  else:
   show_reveal("SAFE! Advance to row %d." % (row_index+1),func():advance_bridge_row())
 else:
  alive[current_player]=false
  crossing+=1
  create_tween().tween_property(panel,"position:y",-6.0,0.75)
  create_tween().tween_property(characters[current_player],"position:y",-7.0,0.9)
  show_reveal("DROP ZONE! %s has fallen!" % contestants[current_player],func():begin_next_contestant())''')
s += '''
func install_branching_bridge() -> void:
 # Expose the drop pit: earlier versions had solid floors covering the water.
 for child in stage.get_children():
  if child is MeshInstance3D and child.mesh is BoxMesh:
   var dimensions:Vector3=child.mesh.size
   if dimensions.x>=27.0 and dimensions.z>=16.0: child.visible=false
   if dimensions.x>10.0 and dimensions.x<11.0 and child.position.y < -2.0: child.visible=false
 for side in [-1.0,1.0]:
  box_mesh(stage,Vector3(side*12.3,-0.9,0),Vector3(14.2,0.3,30.0),Color("121d38"))
 for side in [-1.0,1.0]:
  box_mesh(stage,Vector3(0,-0.9,side*12.3),Vector3(10.4,0.3,5.5),Color("121d38"))
 # Continuously animated, original water imagery on a plane under the bridge.
 var waves=MeshInstance3D.new()
 var plane=PlaneMesh.new()
 plane.size=Vector2(11.0,16.0)
 plane.subdivide_width=50
 plane.subdivide_depth=70
 waves.mesh=plane
 waves.position=Vector3(0,-1.65,0)
 var shader=Shader.new()
 shader.code="""shader_type spatial;
render_mode cull_disabled;
void vertex(){
 VERTEX.y += 0.12*sin(VERTEX.x*2.6+VERTEX.z*1.9+TIME*1.8);
 VERTEX.y += 0.09*cos(VERTEX.x*3.2-VERTEX.z*2.3+TIME*2.4);
}
void fragment(){
 vec2 q=UV*20.0;
 float ripple=sin(q.x*1.45+TIME*1.65+sin(q.y*0.8+TIME))*cos(q.y*0.92-TIME*1.2);
 float foam=smoothstep(0.46,0.78,ripple);
 ALBEDO=mix(vec3(0.009,0.09,0.20),vec3(0.02,0.46,0.70),0.3+0.4*ripple+0.3*foam);
 METALLIC=0.35;
 ROUGHNESS=0.25;
 EMISSION=vec3(0.01,0.20,0.32)*foam*0.5;
}"""
 var mat=ShaderMaterial.new()
 mat.shader=shader
 waves.material_override=mat
 stage.add_child(waves)
 bridge_panels=[]
 var positions_z=[-4.7,-1.6,1.5,4.7]
 for row in range(ROW_COUNTS.size()):
  var row_panels=[]
  var n=int(ROW_COUNTS[row])
  for index in range(n):
   var x=(float(index)-float(n-1)/2.0)*2.52
   var loc=Vector3(x,0.34,float(positions_z[row]))
   var panel=box_mesh(stage,loc,Vector3(2.33,0.22,2.42),Color("157bb4"))
   var body=StaticBody3D.new()
   body.position=loc
   body.collision_layer=1
   body.input_ray_pickable=true
   body.set_meta("row",row)
   body.set_meta("index",index)
   var shape=BoxShape3D.new()
   shape.size=Vector3(2.35,0.45,2.45)
   var collider=CollisionShape3D.new()
   collider.shape=shape
   body.add_child(collider)
   stage.add_child(body)
   var text3d=Label3D.new()
   text3d.text="ANSWER"
   text3d.font_size=38
   text3d.pixel_size=0.005
   text3d.outline_size=6
   text3d.rotation.x=-PI/2.0
   text3d.position=loc+Vector3(0,0.14,0)
   stage.add_child(text3d)
   row_panels.append({"mesh":panel,"body":body,"label":text3d,"position":loc})
  bridge_panels.append(row_panels)

func refresh_bridge_panels() -> void:
 for row in range(bridge_panels.size()):
  for index in range(bridge_panels[row].size()):
   var item:Dictionary=bridge_panels[row][index]
   var mesh:MeshInstance3D=item["mesh"]
   mesh.position=item["position"]
   mesh.material_override=material(Color("1879ad") if row==row_index else Color("183452"))
   var label:Label3D=item["label"]
   if row==row_index and bridge_groups.size()>row:
    label.text=str(bridge_groups[row][index]["label"])
    label.modulate=Color("ffffff")
   else:
    label.text="ROW %d" % (row+1)
    label.modulate=Color("80a5c2")

func advance_bridge_row() -> void:
 refresh_bridge_panels()
 render_bridge()

func _input(event: InputEvent) -> void:
 if not (event is InputEventMouseButton):return
 if event.button_index!=MOUSE_BUTTON_LEFT or not event.pressed:return
 if game_state!="crossing" or awaiting_drop or ai[current_player]:return
 var origin=camera.project_ray_origin(event.position)
 var end=origin+camera.project_ray_normal(event.position)*180.0
 var query=PhysicsRayQueryParameters3D.create(origin,end,1)
 var found=get_world_3d().direct_space_state.intersect_ray(query)
 if found.is_empty():return
 var body=found["collider"]
 if body.has_meta("row") and int(body.get_meta("row"))==row_index:
  select_answer(int(body.get_meta("index")))
'''
p.write_text(s)
print("Patched bridge: 3/3/2/1 branching with animated water.")
