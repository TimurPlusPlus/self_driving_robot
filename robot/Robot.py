import math

class Robot:
    def __init__(self, x1, y1, x2, y2, max_speed=1, sensor_power=5):
        self.x1 = x1
        self.y1 = y1

        self.x2 = x2
        self.y2 = y1

        self.x3 = x2
        self.y3 = y2

        self.x4 = x1
        self.y4 = y2

        self.__max_speed = max_speed
        self.__wheels_distance = math.sqrt((self.x2 - self.x3)**2 + (self.y2 - self.y3)**2)
        self.__sensor_power = sensor_power

    def move(self, track):
        l_velocity, r_velocity = self.scan(track)
        l_velocity *= self.__max_speed
        r_velocity *= self.__max_speed

        if l_velocity == r_velocity:
            self.move_forward(l_velocity)
        else:
            self.rotate(l_velocity, r_velocity)

    def rotate(self, l_velocity, r_velocity):
        velocity = r_velocity
        clock = -1
        cx = (self.x1 + self.x2) / 2                #Middle of the robot's left board
        cy = (self.y1 + self.y2) / 2

        if l_velocity > 0:
            velocity = l_velocity
            cx = (self.x4 + self.x3) / 2            #Right board
            cy = (self.y4 + self.y3) / 2
            clock = 1                               #Rotate clockwise

        omega = velocity / self.__wheels_distance   #Angle speed
        omega *= 180
        omega /= math.pi

        cos = math.cos(omega)
        sin = math.sin(omega)

        self.x1, self.y1 = self.new_coord(self.x1, self.y1, clock, cos, sin, cx, cy)
        self.x2, self.y2 = self.new_coord(self.x2, self.y2, clock, cos, sin, cx, cy)
        self.x3, self.y3 = self.new_coord(self.x3, self.y3, clock, cos, sin, cx, cy)
        self.x4, self.y4 = self.new_coord(self.x4, self.y4, clock, cos, sin, cx, cy)


    def new_coord(self, x, y, clock, cos, sin, cx, cy):
        return (cos * (x - cx) - clock * sin * (y - cy) + cx,
                clock * sin * (x - cx) + cos * (y - cy) + cy)

    def move_forward(self, velocity):
        angle = dx = dy = 0

        if self.y3 == self.y4:
            dx = velocity
        elif self.x3 == self.x4:
            if self.y3 > self.y4:
                dy = velocity
            else:
                dy = -velocity
        else:
            if self.y3 > self.y4:
                angle = math.atan((self.y3 - self.y4) / (self.x3 - self.x4))
                angle *= 180
                angle /= math.pi
                dx = math.cos(angle) * velocity
                dy = math.sin(angle) * velocity
            else:
                angle = math.atan((self.x3 - self.x4) / (self.y4 - self.y3))
                angle *= 180
                angle /= math.pi
                dx = math.sin(angle) * velocity
                dy = -math.cos(angle) * velocity
                print(dx, dy)

        self.x1 += dx
        self.y1 += dy

        self.x2 += dx
        self.y2 += dy

        self.x3 += dx
        self.y3 += dy

        self.x4 += dx
        self.y4 += dy

    def scan(self, track):
        l_signal = self.get_back_signal(track, self.x2, self.y2)
        m_signal = self.get_back_signal(track, (self.x2 + self.x3) / 2, (self.y2 + self.y3) / 2)
        r_signal = self.get_back_signal(track, self.x3, self.y3)
        return self.fuzzyfy(l_signal, m_signal, r_signal)

    def get_back_signal(self, track, sensor_x, sensor_y):
        sum = 0
        n = 0
        for i in range(-self.__sensor_power, self.__sensor_power, 1):
            for j in range(-self.__sensor_power, self.__sensor_power, 1):
                sum += track.getpixel((sensor_x + i, sensor_y + j))[0]
                n += 1
        return sum / n

    def fuzzyfy(self, l_signal, m_signal, r_signal):
        print(l_signal, m_signal, r_signal)
        if r_signal < 150:
            return ((255 - r_signal) / 255 / 5, 0)
        if l_signal < 150:
            return (0, (255 - l_signal) / 255 / 5)
        if m_signal < 150:
            return ((255 - m_signal) / 255, (255 - m_signal) / 255)
        if r_signal < 50 and l_signal < 50:
            return ((255 - m_signal) / 255, (255 - m_signal) / 255)
        return (0, 0)