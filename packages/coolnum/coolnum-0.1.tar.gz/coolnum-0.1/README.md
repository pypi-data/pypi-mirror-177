# 项目介绍

一个把百分数转化成float数的函数

# 作者资料

昵称: jutooy

邮箱: jutooy@qq.com

# 语法

## 导入

    from coolnum import percentToFloat

## 转化百分数

    assert percentToFloat('35%') == 0.35
    assert percentToFloat('3.5%') == 0.035

## 转化千分数

    assert percentToFloat('35‰') == 0.035
    assert percentToFloat('3.5‰') == 0.0035

## 转化int和float型

    assert percentToFloat(3.5) == 3.5
    assert percentToFloat(3) == 3.0

## 转化字符串型

    assert percentToFloat('3.5') == 3.5
    assert percentToFloat('3') == 3.0