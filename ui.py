import pygame

from settings import *


class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # images
        self.bar_bg = pygame.image.load("Assets/Graphics/DG_UI_Bar.png")
        self.weapon_slot = pygame.image.load("Assets/Graphics/DG_UI_WeaponSlot.png")
        self.dialog_bg = pygame.image.load("Assets/Graphics/DG_UI_Dialog.png")

        # ui setup
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.hp_bar_rect = self.bar_bg.get_rect(topleft=(40, 30))
        self.weapon_slot_rect = self.weapon_slot.get_rect(topleft=(50, 580))
        self.weapon_bar_rect = self.bar_bg.get_rect(topleft=(40, 640))
        self.dialog_rect = self.dialog_bg.get_rect(center=(WIDTH//2, 620))

        # dialog setup
        self.dialogs = []
        self.can_pop_dialog = False
        self.dialog_time = pygame.time.get_ticks()

        # self.add_dialog("Hello in new world! Lorem impsum etc.", 3000)
        self.add_dialog("Hello in new world! Lorem impsum etc. Hello in new world! Lorem impsum etc. Hello in new world! Lorem impsum etc. Hello in new world! Lorem impsum etc. Hello in new world! Lorem impsum etc. ", 3000)

    def draw_health_bar(self, current_hp, max_hp, color):
        # draw bg
        self.display_surface.blit(self.bar_bg, self.hp_bar_rect)

        # calculate size
        bg_rect = self.hp_bar_rect.copy()
        ratio = current_hp / max_hp
        current_width = (bg_rect.width-8) * ratio
        current_rect = bg_rect.inflate(-8, -8)
        current_rect.width = current_width

        # text
        text_surf = self.font.render(str(current_hp), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=bg_rect.center)

        # draw the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        self.display_surface.blit(text_surf, text_rect)

    def draw_weapon(self, weapon):
        # draw name bg
        self.display_surface.blit(self.bar_bg, self.weapon_bar_rect)

        # text
        text_surf = self.font.render(f"{weapon.name} Atk: {weapon.atk}", False, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.weapon_bar_rect.center)

        # draw weapon slot
        self.display_surface.blit(self.weapon_slot, self.weapon_slot_rect)

        # weapon scaling ???
        weapon_icon = weapon.surface.copy()
        weapon_icon = pygame.transform.scale(weapon_icon, (64, 64))
        self.display_surface.blit(weapon_icon, self.weapon_slot_rect.inflate(-8, -8))
        # blit weapon img

        # draw weapon ui
        self.display_surface.blit(text_surf, text_rect)

    def draw_dialog(self):
        # check if it has anything to display
        if len(self.dialogs) == 0:
            return

        # draw bg
        self.display_surface.blit(self.dialog_bg, self.dialog_rect)

        # text
        text = self.dialogs[0]["text"]
        # text_surf = self.font.render(f"{text}", False, TEXT_COLOR)
        # text_rect = text_surf.get_rect(topleft=self.dialog_rect.topleft).inflate(-16, -16)
        #
        # # draw text
        # self.display_surface.blit(text_surf, text_rect)

        # draw wraped text
        text_rect = self.dialog_rect.copy().inflate(-32, -24)
        self.drawText(self.display_surface, text, TEXT_COLOR, text_rect, self.font)

    def drawText(self, surface, text, color, rect, font, aa=False, bkg=None):
        # draw some text into an area of a surface
        # automatically wraps words
        # returns any text that didn't get blitted
        # scr: https://www.pygame.org/wiki/TextWrap
        rect = pygame.Rect(rect)
        y = rect.top
        lineSpacing = -2

        # get the height of the font
        fontHeight = font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)

            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

        return text

    def add_dialog(self, text, cooldown=300):
        if len(self.dialogs) == 0 or not self.dialogs[-1] == {"text": text, "cooldown": cooldown}:
            self.dialogs.append({
                "text": text,
                "cooldown": cooldown})
        elif len(self.dialogs) == 1:
            self.dialog_time = pygame.time.get_ticks()

    def pop_dialog(self):
        if not self.can_pop_dialog:
            return
        self.dialogs.pop(0)
        self.can_pop_dialog = False
        self.dialog_time = pygame.time.get_ticks()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if not self.can_pop_dialog:
            if len(self.dialogs) != 0 and current_time-self.dialog_time >= self.dialogs[0]["cooldown"]:
                self.can_pop_dialog = True

    def display(self, player):
        self.cooldowns()
        self.pop_dialog()

        self.draw_health_bar(player.hp, player.max_hp, "red")
        self.draw_weapon(player.weapon)
        self.draw_dialog()
