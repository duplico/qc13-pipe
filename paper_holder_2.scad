
difference() {
    difference() {
        union() {
            cylinder(62, d=64);
            translate([0,-32,0]) cube([10,64,62]);
            translate([-32,-24,0]) cube([4,48,62]);
        }
        translate([10,-32,0]) cube([22,64,62]);
    }
    translate([0,0,1]) {
        difference() {
            cylinder(60, d=62);
            union() {
                translate([0,0,-4.5]) sphere(d=11);
                translate([0,0,58+4.5]) sphere(d=11);
            }
        }
    }
    
    translate([0,0,-2]) difference() {
        cylinder(66,d=60);
        translate([-6.5,-30,-1]) cube([48,60,70]);
    }
}