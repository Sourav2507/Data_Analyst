import matplotlib.pyplot as plt
import base64
from io import BytesIO

def df_scatterplot(df, x_col, y_col, regression=False, color='blue', regression_color='red'):
    plt.scatter(df[x_col], df[y_col], color=color)
    if regression:
        import numpy as np
        m, b = np.polyfit(df[x_col], df[y_col], 1)
        plt.plot(df[x_col], m*df[x_col] + b, linestyle="--", color=regression_color)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"
