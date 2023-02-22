A = 31;
B = 23;
C = 26;
D = 12;
E = 32;
F = 15;
G = 5; // from bottom of servo to top of wires
H = 4; // width of wires
I = 22; // height of body
J = 2; // thickness of wings
K = 5; // width of axel bump
L = 7; // major diameter of arm
M = 4; // minor diameter of arm
N = 14.5; // arm length
O = 1.5; // arm thickness
P = H/3; // width of wire
servo_box_across = D * 4.5;
mount_height = 15; // Needs to be measured exactly
mount_thickness = 20;
mount_across = 130;
mount_cut_across = 112;
inf = 100;
$fn = 50;

module servo_cut() {
    translate([F, 0, -1-P]) cube([inf, D*1.5, inf]);
}

module half() {
    color("Gray") difference() {
        union() {
        // servo_container
        translate([0, 0, -P]) cube([A, servo_box_across, E+P]);
 
        // mount (-Pedro)
        translate([0, -(mount_across - servo_box_across)/2, -mount_height])
            cube([A, mount_across, mount_thickness]);
        }
        
        // mount x-axis cut (-Pedro)
        translate([-1, -(mount_cut_across - servo_box_across)/2, -(mount_height+1)])
            cube([inf, mount_cut_across, mount_height]);

        // z-axis cuts for servos
        translate([-10, D*0.5, 0]) servo_cut();
        translate([-5, D*1.5, 0]) servo_cut();
        translate([0, D*2.5, 0]) servo_cut();
        
        // x-axis cut for servos
        translate([-1, D, (E - B)/2-P]) cube([inf, D*3, B+P]);
    }
    servos();
}

module servo() {
    // body
    color("Blue") translate([0, 0, (E-B)/2]) cube([I, D, B]);
    color("Blue") translate([F, 0, 0]) cube([J, D, E]);
    color("Blue") translate([I, D/2, (E-B)/2+D/2])
        rotate([0, 90, 0]) cylinder(C-I, D/2, D/2);
    color("Blue") translate([I, D/2, E/2])
        rotate([0, 90, 0]) cylinder(C-I, K/2, K/2);
    
    // wire
    color("Red") translate([0, (D-H)/2, (E-B)/2-P]) cube([G, H, P]);
    
    // arm
    color("White") translate([C, D/2, (E-B)/2+D/2])
        rotate([0, 90, 0]) cylinder(A-C, L/2, L/2);
    for (i = [0:0.01:1]) {
        color("White") translate([A-O, D/2, (E-B)/2+D/2-i*N])
            rotate([0, 90, 0]) cylinder(O, L/2*(1-i) + M/2*i,
                                           L/2*(1-i) + M/2*i);
    }
}

module servos() {
    translate([-10, D, 0]) servo();
    translate([-5, D*2, 0]) servo();
    translate([0, D*3, 0]) servo();
}

half();
translate([A*2, D*4.5, 0]) rotate([0, 0, 180]) half();