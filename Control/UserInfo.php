<?php

require_once (PIM_BASE_PATH . '/Control/Controller.php');
require_once (PIM_BASE_PATH . '/Form.php');
require_once (PIM_BASE_PATH . '/View/View.php');

class Control_UserInfo extends Control_Controller
{
	public function execGet()
	{
		return new View_UserInfo();
	}

	public function execPost()
	{
		$fields = Array();
		$ses_companies = Session::get()->companies;

		/* This page is dependent on company data in the Session state */
		if (empty($ses_companies)) {
			/* XXX: throw decent error */
			return;
		}

		$id_form = new IntegerForm("sectoren");
		$identifiers = $id_form->getIntegers();

		$firstname_form = new StringForm("voornaam");
		$firstname = $firstname_form->getString();

		$lastname_form = new StringForm("achternaam");
		$lastname = $lastname_form->getString();

		if (empty($firstname))
			$fields[] = "voornaam";
		if (empty($lastname))
			$fields[] = "achternaam";

		$extras = Array();

		/* For all comppanies in the session state find their corresponding fields */
		$companies = Model_Datahamster::findByIdList($ses_companies);
		foreach ($companies as $c)
			$extras = array_merge($extras, $c->getExtras());

		if (!empty($extras)) {
			foreach ($extras as $extra) {
				$form = new StringForm($extra->getValue());
				$value = $form->getString();
				if (empty($value)) {
					$fields[] = $extra->getValue();
				}
			}
		}

		if (count($fields) == 1) {
			return new View_UserInfo("Voer een " . $fields[0] . " in");
		} else if (count($fields) > 1) {
			$field = array_pop(&$fields);
			$field_list = implode(", ", $fields); 

			return new View_UserInfo("Voer een " . $field_list . " en " . $field . " in");
		}

		/* Success! */
		$this->setLocation("genereer");
	}
}

?>