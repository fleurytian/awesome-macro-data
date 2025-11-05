#!/usr/bin/env python3
"""
验证"政府停摆相当于变相加息"假设

核心假设链条：
1. 政府停摆 → TGA膨胀（财政部积累现金）
2. TGA膨胀 → 银行准备金减少（流动性枯竭）
3. 流动性枯竭 → 短期利率上升（EFFR、SOFR）
4. 短期利率上升 ≈ 变相加息

Usage:
    python verify_shutdown_hypothesis.py us_shutdown_financial_data.xlsx
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 停摆期间定义
SHUTDOWN_PERIODS = [
    {
        'name': '2013年停摆',
        'start': '2013-10-01',
        'end': '2013-10-17',
        'sheet': '1_2013'
    },
    {
        'name': '2018-2019年停摆',
        'start': '2018-12-22',
        'end': '2019-01-25',
        'sheet': '2_2018-2019'
    },
    {
        'name': '2025年停摆',
        'start': '2025-10-01',
        'end': None,  # 持续中
        'sheet': '3_2025'
    }
]


def load_shutdown_data(excel_file, period):
    """加载特定停摆期的数据"""
    try:
        df = pd.read_excel(excel_file, sheet_name=period['sheet'], index_col=0)
        df.index = pd.to_datetime(df.index)
        print(f"✓ 加载 {period['name']} 数据: {len(df)} 条记录")
        return df
    except Exception as e:
        print(f"✗ 加载失败: {e}")
        return None


def calculate_statistics(df, period):
    """计算停摆前、中、后的统计数据"""

    shutdown_start = pd.to_datetime(period['start'])
    shutdown_end = pd.to_datetime(period['end']) if period['end'] else df.index.max()

    # 定义时间段：停摆前30天、停摆期间、停摆后30天
    pre_start = shutdown_start - timedelta(days=30)
    post_end = shutdown_end + timedelta(days=30)

    # 分段数据
    pre_shutdown = df[(df.index >= pre_start) & (df.index < shutdown_start)]
    during_shutdown = df[(df.index >= shutdown_start) & (df.index <= shutdown_end)]
    post_shutdown = df[(df.index > shutdown_end) & (df.index <= post_end)]

    stats = {}

    for col in df.columns:
        stats[col] = {
            'pre_mean': pre_shutdown[col].mean(),
            'during_mean': during_shutdown[col].mean(),
            'post_mean': post_shutdown[col].mean(),
            'pre_to_during_change': None,
            'during_to_post_change': None,
            'pre_to_during_pct': None,
            'during_to_post_pct': None
        }

        # 计算变化
        if not pd.isna(stats[col]['pre_mean']) and not pd.isna(stats[col]['during_mean']):
            stats[col]['pre_to_during_change'] = stats[col]['during_mean'] - stats[col]['pre_mean']
            if stats[col]['pre_mean'] != 0:
                stats[col]['pre_to_during_pct'] = (stats[col]['pre_to_during_change'] / stats[col]['pre_mean']) * 100

        if not pd.isna(stats[col]['during_mean']) and not pd.isna(stats[col]['post_mean']):
            stats[col]['during_to_post_change'] = stats[col]['post_mean'] - stats[col]['during_mean']
            if stats[col]['during_mean'] != 0:
                stats[col]['during_to_post_pct'] = (stats[col]['during_to_post_change'] / stats[col]['during_mean']) * 100

    return stats, pre_shutdown, during_shutdown, post_shutdown


def verify_hypothesis(stats, period):
    """验证假设的各个环节"""

    print(f"\n{'='*70}")
    print(f"假设验证：{period['name']}")
    print(f"{'='*70}")

    results = {
        'hypothesis_1': None,  # TGA是否膨胀
        'hypothesis_2': None,  # 准备金是否减少
        'hypothesis_3': None,  # 利率是否上升
        'overall': None
    }

    # 假设1: 停摆期间TGA是否膨胀？
    tga_col = 'Treasury General Account (TGA)'
    if tga_col in stats:
        tga_change = stats[tga_col]['pre_to_during_pct']
        if tga_change and tga_change > 0:
            results['hypothesis_1'] = True
            print(f"\n✓ 假设1 [验证通过]: TGA在停摆期间膨胀")
            print(f"   停摆前平均: ${stats[tga_col]['pre_mean']/1e9:.2f}B")
            print(f"   停摆期间平均: ${stats[tga_col]['during_mean']/1e9:.2f}B")
            print(f"   变化: +{tga_change:.2f}%")
        else:
            results['hypothesis_1'] = False
            print(f"\n✗ 假设1 [未验证]: TGA未明显膨胀")
            if tga_change:
                print(f"   变化: {tga_change:.2f}%")
    else:
        print(f"\n⚠ 假设1: 缺少TGA数据")

    # 假设2: TGA膨胀时，银行准备金是否减少？
    reserves_col = 'Bank Reserves'
    if reserves_col in stats:
        reserves_change = stats[reserves_col]['pre_to_during_pct']
        if reserves_change and reserves_change < 0:
            results['hypothesis_2'] = True
            print(f"\n✓ 假设2 [验证通过]: 银行准备金在停摆期间减少")
            print(f"   停摆前平均: ${stats[reserves_col]['pre_mean']/1e9:.2f}B")
            print(f"   停摆期间平均: ${stats[reserves_col]['during_mean']/1e9:.2f}B")
            print(f"   变化: {reserves_change:.2f}%")
        else:
            results['hypothesis_2'] = False
            print(f"\n✗ 假设2 [未验证]: 银行准备金未明显减少")
            if reserves_change:
                print(f"   变化: {reserves_change:.2f}%")
    else:
        print(f"\n⚠ 假设2: 缺少银行准备金数据")

    # 假设3: 流动性枯竭时，短期利率是否上升？
    rate_increases = []

    for rate_col in ['Effective Federal Funds Rate (EFFR)',
                      'Secured Overnight Financing Rate (SOFR)']:
        if rate_col in stats:
            rate_change = stats[rate_col]['pre_to_during_change']  # 使用绝对变化（基点）
            if rate_change and rate_change > 0:
                rate_increases.append(True)
                print(f"\n✓ 假设3.{len(rate_increases)} [验证通过]: {rate_col}在停摆期间上升")
                print(f"   停摆前平均: {stats[rate_col]['pre_mean']:.2f}%")
                print(f"   停摆期间平均: {stats[rate_col]['during_mean']:.2f}%")
                print(f"   变化: +{rate_change:.2f} 基点")
            else:
                rate_increases.append(False)
                print(f"\n✗ 假设3.{len(rate_increases)} [未验证]: {rate_col}未明显上升")
                if rate_change:
                    print(f"   变化: {rate_change:.2f} 基点")

    if len(rate_increases) > 0 and any(rate_increases):
        results['hypothesis_3'] = True
    elif len(rate_increases) > 0:
        results['hypothesis_3'] = False
    else:
        print(f"\n⚠ 假设3: 缺少利率数据")

    # 综合判断
    verified = [v for v in results.values() if v is True]
    total = [v for v in results.values() if v is not None]

    if len(verified) == len(total) and len(total) >= 3:
        results['overall'] = "完全验证"
        print(f"\n{'='*70}")
        print(f"🎯 结论: 假设【完全验证】")
        print(f"   政府停摆确实表现出'变相加息'效应")
        print(f"{'='*70}")
    elif len(verified) >= 2:
        results['overall'] = "部分验证"
        print(f"\n{'='*70}")
        print(f"⚠ 结论: 假设【部分验证】")
        print(f"   {len(verified)}/{len(total)} 个环节得到验证")
        print(f"{'='*70}")
    else:
        results['overall'] = "未验证"
        print(f"\n{'='*70}")
        print(f"✗ 结论: 假设【未验证】")
        print(f"   该停摆期未表现出明显的'变相加息'效应")
        print(f"{'='*70}")

    return results


def plot_analysis(df, period, stats, output_file):
    """生成分析图表"""

    shutdown_start = pd.to_datetime(period['start'])
    shutdown_end = pd.to_datetime(period['end']) if period['end'] else df.index.max()

    fig, axes = plt.subplots(4, 1, figsize=(14, 12))
    fig.suptitle(f"{period['name']} - '变相加息'假设验证", fontsize=16, fontweight='bold')

    # 图1: TGA变化
    ax1 = axes[0]
    tga_col = 'Treasury General Account (TGA)'
    if tga_col in df.columns:
        ax1.plot(df.index, df[tga_col]/1e9, linewidth=2, color='#2E86AB', label='TGA')
        ax1.axvspan(shutdown_start, shutdown_end, alpha=0.2, color='red', label='停摆期')
        ax1.set_ylabel('TGA (十亿美元)', fontsize=11)
        ax1.set_title('假设1: 政府停摆 → TGA膨胀', fontsize=12, fontweight='bold')
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)

    # 图2: 银行准备金变化
    ax2 = axes[1]
    reserves_col = 'Bank Reserves'
    if reserves_col in df.columns:
        ax2.plot(df.index, df[reserves_col]/1e9, linewidth=2, color='#A23B72', label='银行准备金')
        ax2.axvspan(shutdown_start, shutdown_end, alpha=0.2, color='red', label='停摆期')
        ax2.set_ylabel('准备金 (十亿美元)', fontsize=11)
        ax2.set_title('假设2: TGA膨胀 → 银行准备金减少', fontsize=12, fontweight='bold')
        ax2.legend(loc='best')
        ax2.grid(True, alpha=0.3)

    # 图3: 短期利率变化 (EFFR)
    ax3 = axes[2]
    effr_col = 'Effective Federal Funds Rate (EFFR)'
    if effr_col in df.columns:
        ax3.plot(df.index, df[effr_col], linewidth=2, color='#F18F01', label='EFFR')
        ax3.axvspan(shutdown_start, shutdown_end, alpha=0.2, color='red', label='停摆期')
        ax3.set_ylabel('EFFR (%)', fontsize=11)
        ax3.set_title('假设3: 流动性枯竭 → 短期利率上升 (EFFR)', fontsize=12, fontweight='bold')
        ax3.legend(loc='best')
        ax3.grid(True, alpha=0.3)

    # 图4: SOFR变化
    ax4 = axes[3]
    sofr_col = 'Secured Overnight Financing Rate (SOFR)'
    if sofr_col in df.columns:
        ax4.plot(df.index, df[sofr_col], linewidth=2, color='#C73E1D', label='SOFR')
        ax4.axvspan(shutdown_start, shutdown_end, alpha=0.2, color='red', label='停摆期')
        ax4.set_ylabel('SOFR (%)', fontsize=11)
        ax4.set_title('假设3: 流动性枯竭 → 短期利率上升 (SOFR)', fontsize=12, fontweight='bold')
        ax4.legend(loc='best')
        ax4.grid(True, alpha=0.3)

    # 格式化x轴
    for ax in axes:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ 图表已保存: {output_file}")

    return fig


def calculate_correlations(df):
    """计算关键变量之间的相关性"""

    print(f"\n{'='*70}")
    print(f"相关性分析")
    print(f"{'='*70}")

    # TGA与银行准备金的相关性
    tga_col = 'Treasury General Account (TGA)'
    reserves_col = 'Bank Reserves'

    if tga_col in df.columns and reserves_col in df.columns:
        # 去除缺失值
        valid_data = df[[tga_col, reserves_col]].dropna()
        if len(valid_data) > 10:
            corr = valid_data[tga_col].corr(valid_data[reserves_col])
            print(f"\nTGA vs 银行准备金:")
            print(f"  相关系数: {corr:.4f}")
            if corr < -0.3:
                print(f"  → 负相关（TGA上升时准备金下降）✓")
            else:
                print(f"  → 相关性不显著")

    # 银行准备金与利率的相关性
    for rate_col in ['Effective Federal Funds Rate (EFFR)',
                     'Secured Overnight Financing Rate (SOFR)']:
        if reserves_col in df.columns and rate_col in df.columns:
            valid_data = df[[reserves_col, rate_col]].dropna()
            if len(valid_data) > 10:
                corr = valid_data[reserves_col].corr(valid_data[rate_col])
                print(f"\n银行准备金 vs {rate_col}:")
                print(f"  相关系数: {corr:.4f}")
                if corr < -0.3:
                    print(f"  → 负相关（准备金下降时利率上升）✓")
                else:
                    print(f"  → 相关性不显著")


def main():
    """主函数"""

    print("\n" + "="*70)
    print("验证假设: '政府停摆相当于变相加息'")
    print("="*70)

    if len(sys.argv) < 2:
        print("\n用法:")
        print(f"  python {sys.argv[0]} us_shutdown_financial_data.xlsx")
        sys.exit(1)

    excel_file = sys.argv[1]

    # 分析每个停摆期
    all_results = {}

    for period in SHUTDOWN_PERIODS:
        df = load_shutdown_data(excel_file, period)

        if df is not None:
            # 计算统计数据
            stats, pre, during, post = calculate_statistics(df, period)

            # 验证假设
            results = verify_hypothesis(stats, period)
            all_results[period['name']] = results

            # 相关性分析
            calculate_correlations(df)

            # 生成图表
            output_chart = f"analysis_{period['sheet']}.png"
            plot_analysis(df, period, stats, output_chart)

    # 总结
    print(f"\n\n{'='*70}")
    print(f"总体结论")
    print(f"{'='*70}")

    for period_name, results in all_results.items():
        print(f"\n{period_name}: {results['overall']}")

    print(f"\n{'='*70}")
    print("分析完成！")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
