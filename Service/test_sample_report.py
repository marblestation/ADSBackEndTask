from __future__ import division
import argparse
import pandas as pd
import numpy as np
from log import setup_logging, logging
setup_logging()
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'font.size': 14})

def plot_score_histogram(refsample_analyzed, resolved, resolved_and_matched, plot_filenames):
    """
    Plot histogram of scores.

    Parameters
    ----------
    refsample_analyzed : Pandas DataFrame
        DataFrame with 'score' field.
    resolved : boolean filter
        True when the row has been resolved.
    resolved_and_matched : boolean filter
        True when the row has been resolved and it matches the expected value.
    plot_filenames : list
        List of filename (strings) where the plot is going to be written.
    """
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(1, 1, 1)
    n, bins, patches = ax.hist(refsample_analyzed.loc[resolved, 'score'], 50, facecolor="black", label="Resolved bibcodes")
    n, bins, patches = ax.hist(refsample_analyzed.loc[resolved_and_matched, 'score'], bins, facecolor="green", label="Matched bibcodes")
    ax.set_xlabel("Score")
    ax.set_ylabel("Count")
    ax.legend(loc='best')
    ax.grid()
    for plot_filename in plot_filenames:
        plt.savefig(plot_filename)
        logging.info("Scores histogram written to '{}'".format(plot_filename))


def read_results(refsample_analysed_filename):
    """
    Read resolved sample of refstrings.

    Parameters
    ----------
    refsample_analysed_filename : string
        Filename with results

    Returns
    -------
    Pandas DataFrame
    """
    refsample_analyzed = pd.read_csv(refsample_analysed_filename, sep="\t")
    refsample_analyzed['score'] = refsample_analyzed['status'].str.extract("(\d+(?:\.\d+)?)")
    refsample_analyzed[['score']] = refsample_analyzed[['score']].apply(pd.to_numeric) # Convert from object to float, needed for plot histogram
    return refsample_analyzed

def get_boolean_filters(refsample_analyzed):
    """
    Create boolean filter identifying connection problems, resolved and matched samples.

    Parameters
    ----------
    refsample_analysed : Pandas DataFrame
        Filename with results

    Returns
    -------
    connection_problem : Boolean filter
        Samples not resolved due to ADS API or network problems.
    not_resolved : Boolean filter
        Samples for which there is no suggested bibcode.
    resolved : Boolean filter
        Samples with suggested bibcode.
    resolved_and_matched : Boolean filter
        Samples with suggested bibcode that matches the expected one.
    """
    connection_problem = refsample_analyzed['status'].isin(["ADS API call failed with an error", "Exception error: 404 != 200", "Exception error: ('Connection aborted.', error(104, 'Connection reset by peer'))"])
    not_resolved = np.logical_and(np.logical_not(connection_problem), refsample_analyzed['suggested_bibcode'].isnull())
    resolved = np.logical_not(refsample_analyzed['suggested_bibcode'].isnull())
    resolved_and_matched = refsample_analyzed['suggested_bibcode'] == refsample_analyzed['bibcode']
    return connection_problem, not_resolved, resolved, resolved_and_matched

def print_report(refsample_analyzed, connection_problem, not_resolved, resolved, resolved_and_matched):
    """
    Print report about resolved and non-resolved samples using the logging system.

    Parameters
    ----------
    refsample_analysed : Pandas DataFrame
        Filename with results
    connection_problem : Boolean filter
        Samples not resolved due to ADS API or network problems.
    not_resolved : Boolean filter
        Samples for which there is no suggested bibcode.
    resolved : Boolean filter
        Samples with suggested bibcode.
    resolved_and_matched : Boolean filter
        Samples with suggested bibcode that matches the expected one.
    """
    n_total = len(refsample_analyzed)
    n_connection_problem = len(refsample_analyzed.loc[connection_problem])
    n_total_analyzed = n_total - n_connection_problem
    n_not_resolved = len(refsample_analyzed.loc[not_resolved])
    n_resolved = len(refsample_analyzed.loc[resolved])
    n_resolved_and_matched = len(refsample_analyzed.loc[resolved_and_matched])
    resolve_rate = n_resolved / n_total_analyzed
    success_rate = n_resolved_and_matched / n_total_analyzed

    logging.info("-"*50)
    logging.info("From the original sample:\n" + \
        "Initial total sample: {}\n".format(n_total) + \
        "Connection problem: {}\n".format(n_connection_problem) + \
        "Total analyzed sample: {}".format(n_total_analyzed))
    logging.info("-"*50)
    logging.info("From the analyzed sample:\n" + \
        "Unable to resolve: {}\n".format(n_not_resolved) + \
        "Resolved: {} ({:.2f}%)\n".format(n_resolved, resolve_rate*100) + \
        "Resolved and matched: {} ({:.2f}%)".format(n_resolved_and_matched, success_rate*100))
    logging.info("-"*50)
    logging.info("Connection problems:\n" + str(refsample_analyzed.loc[connection_problem].groupby(['status'])['bibcode'].agg({'count': len, 'percent':lambda x: np.round((len(x)*1. / n_total_analyzed) * 100, 2)})))
    logging.info("-"*50)
    logging.info("Not resolved:\n" + str(refsample_analyzed.loc[not_resolved].groupby(['status'])['bibcode'].agg({'count': len, 'percent':lambda x: np.round((len(x)*1. / n_total_analyzed) * 100, 2)})))
    logging.info("-"*50)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print a report about the sample process results")
    parser.add_argument('refsample_analysed_filename', action='store', help='Filename with the output from the sample processing (e.g., ReferenceResolver/Tests/output/refsample_analysed.txt)')
    parser.add_argument('plot_filenames', action='store', nargs='+', help='Filename(s) where score histograms will be written (e.g., ReferenceResolver/Tests/output/refsample_analysed_scores_hist.pdf)')
    args = parser.parse_args()

    refsample_analyzed = read_results(args.refsample_analysed_filename)
    connection_problem, not_resolved, resolved, resolved_and_matched = get_boolean_filters(refsample_analyzed)
    print_report(refsample_analyzed, connection_problem, not_resolved, resolved, resolved_and_matched)
    plot_score_histogram(refsample_analyzed, resolved, resolved_and_matched, args.plot_filenames)


