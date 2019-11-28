import re
import sys
import pygame
from pygame.locals import *
import pygame, pygame.font, pygame.event, pygame.draw, string


def path_mark(screen, position, color=(255, 0, 0)):
    pygame.draw.circle(screen, color, position, 2)


def Label_ce(screen, font, text, color, position):
    text_render = font.render(text, True, color)  # 文本样式
    rect = text_render.get_rect()  # 文本位置
    rect.centerx, rect.centery = position
    return screen.blit(text_render, rect)


def Label_co(screen, font, text, color, position):
    text_render = font.render(text, True, color)  # 文本样式
    rect = text_render.get_rect()  # 文本位置
    rect.left, rect.top = position
    return screen.blit(text_render, rect)


# http://www.pygame.org/pcr/inputbox/
# def enter(screen, position, question, font, boxcolor=(0, 0, 0), textcolor=(255, 255, 255),
#           bwidth=200, bheigh=50):
#     current_string = []
#     pygame.display.update()
#     while True:
#         while True:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit(-1)
#                 if event.type == KEYDOWN:
#                     inkey = event.key;
#                     if inkey == K_BACKSPACE:
#                         current_string = current_string[0:-1]
#                     elif inkey == K_RETURN:
#                         break
#                     elif inkey <= 127:
#                         current_string.append(chr(inkey))
#                     else:
#                         pass
#                     Button(screen, position, question + ':' + "".join(current_string), font, boxcolor, textcolor,
#                            bwidth, bheigh)
#                     pygame.display.update()
#                 else:
#                     pass
#     return "".join(current_string)


def check_setted(cfg):
    setted = [False, False, False, False]
    if 0 < cfg['Rows'] <= 35:
        setted[0] = True
    if 0 < cfg['Cols'] <= 50:
        setted[1] = True
    if 0 <= cfg['Starting point'][0] < cfg['Rows'] and 0 <= cfg['Starting point'][1] < cfg['Cols']:
        setted[2] = True
    if 0 <= cfg['Destination'][0] < cfg['Rows'] and 0 <= cfg['Destination'][1] < cfg['Cols']:
        setted[3] = True
    return setted


def InputBox(screen, font, focus, question, ans, hint, color, position, max):
    font.set_italic(focus)
    # 求空格数
    width, height = font.size(question + ans + hint)
    blank = (max - position[0] - width) // 2 // 25
    left = (max - position[0] - width - blank * 25) // 25
    # question
    rect = Label_co(screen, font, question, color, position)
    x, y = rect.left + rect.width, rect.top
    font.set_underline(focus)
    rect2 = Label_co(screen, font, ' ' * blank + ans + ' ' * left, color, (x, y))
    font.set_underline(False)
    Label_co(screen, font, hint, color, (rect2.left + rect2.width, y))
    font.set_italic(False)
    return rect


def setting(screen, cfg):
    # 字体样式
    font_title = pygame.font.SysFont(cfg.FONT, 80)
    font = pygame.font.SysFont(cfg.FONT2, 45)
    font_start = pygame.font.SysFont(cfg.FONT, 70)
    # 设置
    cfgs = {'Rows': cfg.MAZESIZE[0], 'Cols': cfg.MAZESIZE[1], 'Starting point': cfg.STARTPOINT,
            'Destination': cfg.DESTINATION}
    # 设置是否正确
    setted = check_setted(cfgs)
    focus = ['title', 'Rows', 'Cols', 'Starting point', 'Destination']
    hint = {'Rows': '(0<rows<=35)', 'Cols': '(0 < cols <= 50)', 'Starting point': '', 'Destination': ''}
    focused = 1
    # current_string=str(cfgs[focus[focused]])
    current_string=[]
    while True:
        screen.fill(cfg.BACKGROUND)
        # 标题
        # 输入框
        labels = {'title': Label_co(screen, font_title, 'Setting:', cfg.FOREGROUND, (10, 0)),
                   'Rows': None, 'Cols': None, 'Starting point': None, 'Destination': None}
        pygame.draw.line(screen, cfg.LINE, (0, labels['title'].top + labels['title'].height - 20),
                         (labels['title'].left + labels['title'].width + 400,
                          labels['title'].top + labels['title'].height - 20))
        for i in range(1, 5):
            if i == focused:
                labels[focus[focused]] = InputBox(screen, font, True, focus[focused] + ': ', str(cfgs[focus[focused]]),
                                                   hint[focus[focused]], cfg.HIGHLIGHT,
                                                   (20, labels[focus[focused - 1]].top + labels[
                                                       focus[focused - 1]].height + 30),
                                                   cfg.SCREENSIZE[0])
            else:
                labels[focus[i]] = InputBox(screen, font, False, focus[i] + ': ', str(cfgs[focus[i]]), hint[focus[i]],
                                             cfg.FOREGROUND,
                                             (20, labels[focus[i - 1]].top + labels[focus[i - 1]].height + 30),
                                             cfg.SCREENSIZE[0])
        warning = Label_co(screen, font, '', cfg.HIGHLIGHT, (10, cfg.SCREENSIZE[1] - font_title.size('')[1] - 20))
        start = Label_ce(screen, pygame.font.SysFont(cfg.FONT, 70), 'Start', cfg.FOREGROUND,
                         (cfg.SCREENSIZE[0] // 2, cfg.SCREENSIZE[1] - font_title.size('')[1] // 2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(-1)
            if event.type == KEYDOWN:
                inkey = event.key
                if inkey == K_BACKSPACE:
                    current_string = current_string[0:-1]
                elif inkey == K_RETURN or inkey == K_RIGHT:
                    setted = check_setted(cfgs)
                    if setted.count(True) != 4:
                        warning = Label_co(screen, font, '输入有错', cfg.HIGHLIGHT,
                                           (10, cfg.SCREENSIZE[1] - font_title.size('')[1] - 20))
                    else:
                        pass
                elif inkey <= 127:
                    current_string.append(chr(inkey))
                else:
                    pass
                pygame.display.update()
            else:
                pass
        pygame.display.update()


def Interface(screen, cfg, mode='game_start', title='Maze'):
    # 字体样式
    font_title = pygame.font.SysFont(cfg.FONT, 120)  # 标题字体
    # font_title_min = pygame.font.SysFont(cfg.FONT, 25)  # 标题字体
    font = pygame.font.SysFont(cfg.FONT, 55)  # 按钮字体
    font.set_underline(True)  # 开启下划线
    font_focus = pygame.font.SysFont(cfg.FONT, 100)  # 焦点按钮字体
    # 按钮样式
    label_title = {'font': font_title, 'font_focus': font_title, 'text': title, 'color': cfg.HIGHLIGHT,
                   'position': ((cfg.SCREENSIZE[0]) // 2, cfg.SCREENSIZE[1] // 4)}
    label_continue = {'font': font, 'font_focus': font_focus, 'text': 'Start', 'color': cfg.FOREGROUND,
                      'position': ((cfg.SCREENSIZE[0]) // 2, cfg.SCREENSIZE[1] // 2)}
    label_quit = {'font': font, 'font_focus': font_focus, 'text': 'Quit', 'color': cfg.FOREGROUND,
                  'position': ((cfg.SCREENSIZE[0]) // 2, cfg.SCREENSIZE[1] - cfg.SCREENSIZE[1] // 3)}
    label_format = {'title': label_title, 'continue': label_continue, 'quit': label_quit}
    # 按钮
    buttons = {'title': None, 'continue': None, 'quit': None}

    image = pygame.image.load(cfg.HEROPICPATH)
    image = pygame.transform.scale(image, (50, 50))
    rect = image.get_rect()

    if mode == 'game_switch':
        label_continue['text'] = 'Next'
    elif mode == 'game_end':
        label_continue['text'] = 'Restart'
    clock = pygame.time.Clock()
    screen.fill(cfg.BACKGROUND)
    for key in buttons.keys():
        buttons[key] = Label_ce(screen, label_format[key]['font'], label_format[key]['text'],
                                label_format[key]['color'],
                                label_format[key]['position'])
    pygame.draw.line(screen, cfg.LINE,
                     (buttons['title'].left - 100, buttons['title'].top + buttons['title'].height - 40), (
                         buttons['title'].left + buttons['title'].width + 100,
                         buttons['title'].top + buttons['title'].height - 40))
    rect.centerx, rect.centery = buttons['title'].centerx + buttons['title'].width // 2 + 25, buttons[
        'title'].centery + 30
    screen.blit(image, rect)
    while True:
        screen.fill(cfg.BACKGROUND)
        for key in buttons.keys():
            if buttons[key].collidepoint(pygame.mouse.get_pos()):
                # screen.fill(cfg.BACKGROUND)
                # buttons['title'] = Label(screen, label_format[key]['font_focus'], label_format['title']['text'],
                #                          label_format['title']['color'], label_format['title']['position'])
                buttons[key] = Label_ce(screen, label_format[key]['font_focus'], label_format[key]['text'],
                                        label_format[key]['color'], label_format[key]['position'])
            else:
                buttons[key] = Label_ce(screen, label_format[key]['font'], label_format[key]['text'],
                                        label_format[key]['color'], label_format[key]['position'])
        pygame.draw.line(screen, cfg.LINE,
                         (buttons['title'].left - 100, buttons['title'].top + buttons['title'].height - 40), (
                             buttons['title'].left + buttons['title'].width + 100,
                             buttons['title'].top + buttons['title'].height - 40))
        screen.blit(image, rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(-1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons['continue'].collidepoint(pygame.mouse.get_pos()):
                    return True
                elif buttons['quit'].collidepoint(pygame.mouse.get_pos()):
                    return False
        pygame.display.update()
        clock.tick(cfg.FPS)
