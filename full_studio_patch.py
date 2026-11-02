from pathlib import Path
p=Path("DropZone_Godot4/scripts/main.gd")
s=p.read_text()
if "func enhance_full_studio()" in s:
    raise SystemExit(0)
s=s.replace(" create_world()\n create_ui()", " create_world()\n enhance_full_studio()\n create_ui()",1)
s += r'''

# Full broadcast studio: procedural geometry included in exports
func neon(parent: Node3D, pos: Vector3, size: Vector3, color: Color) -> void:
 var obj=box_mesh(parent,pos,size,color)
 var m=material(color,0.2)
 m.emission_enabled=true
 m.emission=color
 m.emission_energy_multiplier=2.5
 obj.material_override=m

func sign_text(text_value: String, pos: Vector3, font_size: int, color: Color) -> void:
 var label=Label3D.new()
 label.text=text_value
 label.font_size=font_size
 label.pixel_size=0.006
 label.modulate=color
 label.outline_size=9
 label.outline_modulate=Color("020617")
 label.position=pos
 stage.add_child(label)

func studio_omni(pos: Vector3, color: Color) -> void:
 var light=OmniLight3D.new()
 light.position=pos
 light.light_color=color
 light.light_energy=2.2
 light.omni_range=18
 stage.add_child(light)

func enhance_full_studio() -> void:
 # Entire-studio envelope, stage wings and rear branded LED wall
 box_mesh(stage,Vector3(0,-1.4,0),Vector3(39,0.4,34),Color("060a19"))
 box_mesh(stage,Vector3(0,4.3,-12.2),Vector3(35,11,0.4),Color("0a1630"))
 for x in [-17.0,17.0]:
  box_mesh(stage,Vector3(x,4.5,0),Vector3(0.4,11,29),Color("0e1d39"))
  for z in [-8.0,-3.0,2.0,7.0]:
   neon(stage,Vector3(x*0.96,3.4,z),Vector3(0.13,7.0,0.14),Color("167ac1"))
 box_mesh(stage,Vector3(0,3.65,-11.7),Vector3(21.3,6.0,0.35),Color("08132a"))
 box_mesh(stage,Vector3(0,3.7,-11.43),Vector3(19.5,5.1,0.12),Color("123573"))
 neon(stage,Vector3(0,6.7,-11.4),Vector3(22.0,0.19,0.24),Color("2fe1ff"))
 for x in [-10.75,10.75]:
  neon(stage,Vector3(x,3.7,-11.4),Vector3(0.19,6.15,0.23),Color("2fe1ff"))
 sign_text("D R O P    Z O N E",Vector3(0,4.2,-11.20),94,Color("b6f7ff"))
 sign_text("THE BRIDGE  /  THE VAULT",Vector3(0,2.5,-11.19),35,Color("f9d27a"))
 # Four original concentric suspended Millionaire-inspired ceiling light rigs
 for radius in [8.0,10.5,13.0,15.2]:
  var ring=MeshInstance3D.new()
  var torus=TorusMesh.new()
  torus.inner_radius=radius-0.13
  torus.outer_radius=radius+0.13
  ring.mesh=torus
  var rm=material(Color("25a5ed"))
  rm.emission_enabled=true
  rm.emission=Color("2eafe7") if radius<14.0 else Color("e3bd66")
  rm.emission_energy_multiplier=3.1
  ring.material_override=rm
  ring.position=Vector3(0,9.9+(15.2-radius)*0.1,0)
  stage.add_child(ring)
  for n in range(12):
   var a=TAU*n/12.0
   var spoke=box_mesh(stage,Vector3(cos(a)*radius*0.5,ring.position.y+0.08,sin(a)*radius*0.5),Vector3(radius,0.10,0.08),Color("263653"))
   spoke.rotation.y=-a
 for x in [-12.0,-6.0,6.0,12.0]:
  for z in [-7.0,7.0]:
   box_mesh(stage,Vector3(x,11.0,z),Vector3(0.08,2.5,0.08),Color("8ba1b8"))
 # Deep central pit with illuminated safe-bridge railings
 box_mesh(stage,Vector3(0,-2.6,0),Vector3(10.6,0.2,16),Color("010510"))
 for x in [-5.3,5.3]:
  box_mesh(stage,Vector3(x,-1.2,0),Vector3(0.2,2.5,16),Color("102c5a"))
  for z in [-6.8,-4.8,-2.8,-0.8,1.2,3.2,5.2,7.2]:
   neon(stage,Vector3(x,-0.33,z),Vector3(0.13,0.12,1.1),Color("12adff"))
 for x in [-3.98,3.98]:
  neon(stage,Vector3(x,0.17,0),Vector3(0.11,0.09,13.2),Color("3be5ff"))
 for i in range(9):
  neon(stage,Vector3(0,0.16,float(i)*1.5-6.04),Vector3(7.75,0.05,0.07),Color("68d7fb"))
 for z in [-7.5,7.75]:
  box_mesh(stage,Vector3(0,0.27,z),Vector3(9.7,0.24,2.1),Color("234775"))
  neon(stage,Vector3(0,0.40,z),Vector3(9.5,0.06,0.12),Color("e7c56a"))
 # Host podium and lit contestant introduction bay camera-left
 box_mesh(stage,Vector3(-10.7,-0.24,0.2),Vector3(4.6,0.48,6.1),Color("1e3a66"))
 box_mesh(stage,Vector3(-10.7,0.90,0.4),Vector3(2.4,1.55,1.25),Color("102b51"))
 box_mesh(stage,Vector3(-10.7,1.73,0.4),Vector3(2.7,0.18,1.43),Color("cfb77d"))
 neon(stage,Vector3(-10.7,0.98,1.07),Vector3(2.05,0.16,0.08),Color("25cfff"))
 sign_text("KARLI-RAE",Vector3(-10.7,1.17,1.09),29,Color("fff0cf"))
 sign_text("HOST",Vector3(-10.7,3.15,-2.8),36,Color("91e8ff"))
 # Vault station camera-right with permanent game-specific illuminated signage
 box_mesh(stage,Vector3(11.6,-0.25,0),Vector3(5.7,0.55,7),Color("292b4d"))
 box_mesh(stage,Vector3(11.6,2.65,-2.9),Vector3(5.3,3.6,0.25),Color("111b36"))
 for x in [8.8,14.4]:
  neon(stage,Vector3(x,2.7,-2.72),Vector3(0.16,4.5,0.14),Color("f4bd58"))
 neon(stage,Vector3(11.6,4.93,-2.72),Vector3(5.75,0.16,0.14),Color("f4bd58"))
 sign_text("THE VAULT",Vector3(11.6,3.72,-2.71),57,Color("ffe09a"))
 sign_text("REVIVE ONE PLAYER",Vector3(11.6,2.6,-2.70),27,Color("ffffff"))
 sign_text("HALVE THE BANK",Vector3(11.6,1.93,-2.70),27,Color("ffd270"))
 box_mesh(stage,Vector3(11.6,0.70,1.0),Vector3(2.9,1.3,1.8),Color("494166"))
 neon(stage,Vector3(11.6,1.39,1),Vector3(3.1,0.09,2.0),Color("f4bf5c"))
 # Curved grandstand impression, spectator silhouettes and light aisle divisions
 for side in [-1,1]:
  for r in range(4):
   var sx=float(side)*(11.2+float(r)*1.14)
   for n in range(10):
    var z=-7.2+float(n)*1.6
    var h=0.5+float(r)*0.48
    box_mesh(stage,Vector3(sx,h,z),Vector3(0.82,0.22,0.86),Color("244374"))
    box_mesh(stage,Vector3(sx+float(side)*0.25,h+0.32,z),Vector3(0.15,0.69,0.85),Color("2f507e"))
    if (n+r)%3 != 0:
     box_mesh(stage,Vector3(sx,h+0.61,z),Vector3(0.43,0.63,0.37),Color("384e69") if n%2==0 else Color("5a466a"))
     var head=MeshInstance3D.new()
     var sphere=SphereMesh.new()
     sphere.radius=0.19
     sphere.height=0.38
     head.mesh=sphere
     head.material_override=material(Color("b99a85"))
     head.position=Vector3(sx,h+1.13,z)
     stage.add_child(head)
 # Camera pedestals / audience-side moving-head light proxies
 for x in [-13.5,13.5]:
  box_mesh(stage,Vector3(x,0.45,10.1),Vector3(1.15,0.9,1.45),Color("162743"))
  box_mesh(stage,Vector3(x,1.5,10.1),Vector3(0.75,1.2,0.8),Color("10192f"))
  neon(stage,Vector3(x,2.05,9.68),Vector3(0.35,0.12,0.08),Color("37b9fd"))
 for p in [Vector3(-11,6,3),Vector3(11,6,3),Vector3(0,8,-7),Vector3(0,8,8)]:
  studio_omni(p,Color("65b9ff"))
 camera.position=Vector3(23,15,25)
 camera.look_at(Vector3(0,2,-1),Vector3.UP)
'''
p.write_text(s)
print("Full broadcast set installed")
