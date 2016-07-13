
difference() {
    difference() {
        union() {
            cylinder(62, d=64);
            translate([0,-32,0]) cube([10,64,62]);
            translate([-32,-24,0]) cube([4,48,62]);
        }
        translate([10,-32,0]) cube([22,64,62]);
    }
    translate([0,0,2]) {
        difference() {
            cylinder(58, d=60);
            union() {
                translate([0,0,-3]) sphere(d=11);
                translate([0,0,58+3]) sphere(d=11);
            }
        }
    }
    
    translate([0,0,-2]) difference() {
        cylinder(66,d=60);
        translate([-10,-30,-1]) cube([48,60,70]);
    }
}