import seaborn as sns
import matplotlib.pyplot as plt


def ax_params(xlabel, ylabel, plt_title=None, ax=None, legend_title=None, c='k', savefig=False):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    # plt.title(plt_title)
    if legend_title:
        plt.legend(title=legend_title,loc='best')
    if ax is None:
        ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_color(c)
    ax.spines['bottom'].set_color(c)
    if savefig:
        plt.gcf().savefig(f'{plt_title}.png',
                          dpi=200,  transparent=True, bbox_inches='tight')


def distplot(column, data=None, xlabel=None, ylabel=None,
             plt_title=None, ax=None, legend_title=None, c='k',
             savefig=False):
    for b,h,t in [(0,'#1a9988', 'Current'),(1,'#eb5600','Delinquent')]:
        sns.distplot(data[column][data['delinquency_bool'] == t],
                     color=h, label=t, bins=10, kde=False,
                     norm_hist=True)

    ax_params(xlabel, ylabel, plt_title=plt_title, ax=ax,
              legend_title=legend_title, c=c, savefig=savefig)
