distances_in = 8 : 4 : 44;
sensor_reading = [490, 385, 300, 240, 210, 185, 170, 157, 153, 145];

% convert to right units
distances_cm = 2.54*distances_in;
sensor_voltage = sensor_reading*5/1023;

hold on;
plot(1./distances_cm, sensor_voltage);
title("Sensor Voltage Readings vs. Distance")
xlabel("Distance, cm");
ylabel("Sensor Voltage Reading, V");


coefficients = polyfit(1./distances_cm, sensor_voltage, 1);

xFit = linspace(min(1./distances_cm), max(1./distances_cm), 1000);
yFit = polyval(coefficients, xFit);

hold on; % Set hold on so the next plot does not blow away the one we just drew.
plot(xFit, yFit, 'r-', 'LineWidth', 2); % Plot fitted line.
grid on;
hold off;
