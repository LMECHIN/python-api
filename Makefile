SRC	=	main.py

NAME = server-api

all: $(NAME)

$(NAME):
	cp $(SRC) $(NAME) && chmod +x $(NAME)

fclean:
	rm -f $(NAME)

re: fclean all
