distances_in = 8 : 4 : 44;
sensor_reading = [490, 385, 300, 240, 210, 185, 170, 157, 153, 145];

% convert to right units
distances_cm = 2.54*distances_in;
sensor_voltage = sensor_reading*5/1023;

plot(distances_cm, sensor_voltage);
title("Sensor Voltage Readings vs. Distance")
xlabel("Distance, cm");
ylabel("Sensor Voltage Reading, V");
