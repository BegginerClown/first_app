
class IsCanMove:
    def can_move_x(self, x, y):
        if y >= 473:
            return 148 <= x <= 1200
        elif y >= 446:
            return 148 <= x <= 844
        elif y > 410:
            return 404 <= x <= 676
        else:
            return True

    def can_move_y(self, x, y):
        if x >= 864:
            return 552 <= y <= 474
