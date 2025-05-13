#!/usr/bin/env python
"""
MarkupSafe版本兼容性修复

此脚本用于解决某些Flask应用程序与新版本MarkupSafe之间的兼容性问题。
当新版本的MarkupSafe与旧版本的Flask一起使用时可能会出现此问题。

此脚本通过修改导入路径和添加必要的属性来模拟旧版本的行为。
"""

import sys
import importlib
import logging

logger = logging.getLogger(__name__)

def apply_markupsafe_fix():
    """
    应用MarkupSafe的兼容性修复
    """
    try:
        import markupsafe
        
        # 检查是否需要修复
        if not hasattr(markupsafe, 'Markup') or not hasattr(markupsafe.Markup, 'escape'):
            logger.info("正在应用MarkupSafe修复...")
            
            # 为缺失的属性和方法添加填充
            if not hasattr(markupsafe, 'Markup'):
                markupsafe.Markup = markupsafe.Markup_
            
            if hasattr(markupsafe, 'Markup') and not hasattr(markupsafe.Markup, 'escape'):
                markupsafe.Markup.escape = markupsafe.escape
                
            if hasattr(markupsafe, 'Markup') and not hasattr(markupsafe.Markup, 'unescape'):
                markupsafe.Markup.unescape = markupsafe.unescape
            
            logger.info("MarkupSafe修复已应用")
        else:
            logger.info("MarkupSafe不需要修复")
            
    except (ImportError, AttributeError) as e:
        logger.error(f"应用MarkupSafe修复时出错: {e}")
        return False
        
    return True

# 当作为独立脚本运行时应用修复
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if apply_markupsafe_fix():
        print("MarkupSafe修复已成功应用")
    else:
        print("无法应用MarkupSafe修复")
else:
    # 当作为模块导入时自动应用修复
    apply_markupsafe_fix() 