import click
import psutil


@click.command()
@click.option('--pid', type=int, help='Specifies the id of the process')
def main(pid: int):
    assert isinstance(pid, int)
    process = psutil.Process(pid)
    click.echo(f'process name is: {process.name()}')


if __name__ == '__main__':
    main()
