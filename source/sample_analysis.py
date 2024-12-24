import json
import pandas as pd
import matplotlib.pyplot as plt
if __name__ == '__main__':
    path = r'C:\Users\Murilo\Desktop\Projetos\TCC\ConsolidatedData\data.json'
    with open(path) as f:
        data = json.load(f)
    df = pd.DataFrame(data)

    # Calculate counts and percentages
    label_counts = df['label'].value_counts()
    label_percentages = df['label'].value_counts(normalize=True) * 100

    # Plot the counts
    fig, ax = plt.subplots()
    bars = ax.bar(label_counts.index, label_counts, color=['skyblue', 'salmon'])

    # Add percentage annotations on top of each bar
    for bar, count, percentage in zip(bars, label_counts, label_percentages):
        bar_height = bar.get_height()
        center_y = bar_height / 2
    
        # Add count label
        ax.annotate(f'{count}', 
                    xy=(bar.get_x() + bar.get_width() / 2, center_y), 
                    xytext=(0, -5),  # Offset slightly down for separation
                    textcoords="offset points",
                    ha='center', va='center', color='black', weight='bold')
        
        # Add percentage label just below the count
        ax.annotate(f'({percentage:.1f}%)', 
                    xy=(bar.get_x() + bar.get_width() / 2, center_y - 20), 
                    xytext=(0, 20),  # Offset slightly to avoid overlap with count
                    textcoords="offset points",
                    ha='center', va='center', color='gray')

    # Add labels and title
    ax.set_xlabel('Label')
    ax.set_ylabel('Count')
    plt.show()