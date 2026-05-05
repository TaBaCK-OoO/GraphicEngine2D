def print_gimbal_lock_derivation():
    print("--- Завдання 4: Математичне виведення Gimbal Lock ---\n")

    print("   Загальний вигляд матриці R = Rz(gamma) * Ry(beta) * Rx(alpha)")
    print("   Rx(alpha) = [[1, 0, 0],")
    print("                [0, cos(a), -sin(a)],")
    print("                [0, sin(a), cos(a)]]")
    print("   Ry(beta)  = [[cos(b), 0, sin(b)],")
    print("                [0, 1, 0],")
    print("                [-sin(b), 0, cos(b)]]")
    print("   Rz(gamma) = [[cos(g), -sin(g), 0],")
    print("                [sin(g), cos(g), 0],")
    print("                [0, 0, 1]]\n")

    print("   Підставимо beta = 90 градусів (pi/2):")
    print("   cos(90) = 0, sin(90) = 1")
    print("   Ry(90) = [[0, 0, 1],")
    print("             [0, 1, 0],")
    print("             [-1, 0, 0]]\n")

    print("   Перемножимо Rz(gamma) * Ry(90) * Rx(alpha):")
    print("   R = [[0, sin(a)*sin(g) + cos(a)*cos(g), cos(a)*sin(g) - sin(a)*cos(g)],")
    print("        [0, sin(a)*cos(g) - cos(a)*sin(g), cos(a)*cos(g) + sin(a)*sin(g)],")
    print("        [-1, 0, 0]]\n")

    print("   Спрощення за тригонометричними тотожностями:")
    print("   cos(a-g) = cos(a)cos(g) + sin(a)sin(g)")
    print("   sin(a-g) = sin(a)cos(g) - cos(a)sin(g)")
    print("   -sin(a-g) = cos(a)sin(g) - sin(a)cos(g)\n")

    print("   Спрощена результуюча матриця:")
    print("   R = [[ 0,  cos(a-g), -sin(a-g) ]")
    print("        [ 0,  sin(a-g),  cos(a-g) ]")
    print("        [-1,  0,         0        ]]\n")

    print("   Доведення:")
    print("   Як бачимо, фінальна матриця обертання залежить виключно від різниці (alpha - gamma).")
    print("   Це означає, що зміна кута alpha на X та кута gamma на Z дають однаковий ефект обертання.")
    print("   Осі X та Z збіглися у просторі (склеїлися), що призвело до втрати одного ступеня вільності.")
    print("   Цей стан і називається Gimbal Lock.")


if __name__ == '__main__':
    print_gimbal_lock_derivation()